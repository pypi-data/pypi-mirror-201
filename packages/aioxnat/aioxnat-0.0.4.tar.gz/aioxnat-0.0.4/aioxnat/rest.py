import enum
import abc, typing

import httpx

from aioxnat import objects


Ta = typing.TypeVar("Ta")

_MappingSeries = typing.Sequence[typing.Mapping[str, str]]
_AsyncChunkGenerator = typing.AsyncGenerator[typing.Sequence[Ta], None]


class HasURI(typing.Protocol):

    @property
    def URI(self) -> str:
        ...


class HasURL(typing.Protocol):

    @property
    def URL(self) -> str:
        ...


async def _aiter(it: typing.Iterable[Ta]):
    for item in it:
        yield item


def _join_uri(api: HasURI | HasURL, *parts: str):
    url = (api.URL if hasattr(api, "URL") else api.URI)
    return "/".join([url, *parts])


def _join_columns(*parts: str):
    return ",".join(parts)


def _parse_rest_result(response: httpx.Response) -> _MappingSeries:
    return response.json()["ResultSet"]["Result"]


class WebProtocol(enum.StrEnum):
    HTTP = "http"
    HTTPS = "https"


class ResourceAction(enum.Enum):
    REFRESH = enum.auto()
    DELETE = enum.auto()
    CREATE = enum.auto()


class AsyncRestAPI(typing.Protocol):

    @property
    @abc.abstractmethod
    def URL(self) -> str:
        """
        URL pointing to the target host. This
        includes the protocol.
        """

    @abc.abstractmethod
    def get_experiments(self,
                        project_name: str,
                        *,
                        chunk_size: typing.Optional[int]) -> _AsyncChunkGenerator[objects.Experiment]:
        """
        Retrieves experiment data from a
        particular project.
        """

    @typing.overload
    @abc.abstractmethod
    def get_scans(self,
                        experiment_or_project: str, /) -> _AsyncChunkGenerator[objects.Scan]:
        ...

    @typing.overload
    @abc.abstractmethod
    def get_scans(self,
                        experiment_or_project: objects.Experiment, /) -> _AsyncChunkGenerator[objects.Scan]:
        ...

    @typing.overload
    @abc.abstractmethod
    def get_scans(self,
                  experiment_or_project: str,
                  *,
                  chunk_size: typing.Optional[int]) -> _AsyncChunkGenerator[objects.Scan]:
        ...

    @typing.overload
    @abc.abstractmethod
    def get_scans(self,
                  experiment_or_project: objects.Experiment,
                  *,
                  chunk_size: typing.Optional[int]) -> _AsyncChunkGenerator[objects.Scan]:
        ...

    @abc.abstractmethod #type: ignore[misc]
    def get_scans(self,
                  experiment_or_project: objects.Experiment | str,
                  *,
                  chunk_size: typing.Optional[int]) -> _AsyncChunkGenerator[objects.Scan]:
        """
        Retrieves scans related to a particular
        experiment.
        """

    @typing.overload
    @abc.abstractmethod
    async def resources(self, scan: objects.Scan, /) -> _MappingSeries:
        """Retrieves resources from a scan."""

    @typing.overload
    @abc.abstractmethod
    async def resources(self,
                        scan: objects.Scan,
                        name: str, /) -> typing.Sequence[objects.FileData]:
        """
        Retrieves resource data from a scan.
        """

    @typing.overload
    @abc.abstractmethod
    async def resources(self,
                        scan: objects.Scan,
                        name: str,
                        action: ResourceAction,
                        **params: str) -> None:
        """
        Perform the given action on a resource
        belonging to a scan.
        """

    @abc.abstractmethod
    async def resources(self,
                            scan: objects.Scan,
                            name: typing.Optional[str] = None,
                            action: typing.Optional[ResourceAction] = None,
                            **params: str) -> _MappingSeries | typing.Sequence[objects.FileData] | None:
        ...

    @classmethod
    @abc.abstractmethod
    def build_client(cls, api: typing.Self) -> httpx.Client:
        """Builds a raw client object."""

    @abc.abstractmethod
    async def __aenter__(self) -> typing.Self:
        ...

    async def __aexit__(self, *exc_details):
        ...


class SimpleAsyncRestAPI(AsyncRestAPI):
    _hostname: str
    _username: str
    _password: str
    _protocol: WebProtocol
    _port_number: typing.Optional[int]

    _client: httpx.AsyncClient

    _timeouts: tuple[float, float] = (10.0, 5 * 60.0) # (connect, read) timeouts

    @property
    def URL(self):
        url = f"{self._protocol!s}://{self._hostname}"
        return url + (f":{self._port_number}" if self._port_number else "")

    async def get_experiments(self,
                        project_name: str,
                        *,
                        chunk_size: typing.Optional[int] = None):
        chunk_size = chunk_size or 16
        columns = _join_columns(
            "xnat:subjectassessordata/id",
            "subject_label",
            "label",
            "project",
            "xsiType",
            "URI")
        url = _join_uri(self, "data", "projects", project_name, "experiments")
        res = (await self._client.get(url,
                        follow_redirects=True,
                        timeout=self._timeouts, #type: ignore[arg-type]
                        params={"format": "json", "columns": columns}))
        res.raise_for_status()
        results = res.json()["ResultSet"]["Result"]

        position   = 0
        make_chunk = lambda p: [
            objects.Experiment.from_mapping(r)
            for r in results[p:p+chunk_size]]

        while data := make_chunk(position):
            yield tuple(data)
            position += chunk_size

    async def get_scans(self,
                    experiment_or_project: objects.Experiment | str,
                    *,
                    chunk_size: typing.Optional[int] = None):
        chunk_size = chunk_size or 16
        experiments = self._parse_exp_or_pjt(experiment_or_project)

        def make_chunk(ex, rlt, p):
            for r in rlt[p:p+chunk_size]:
                r["experiment"] = ex
            return [objects.Scan.from_mapping(r) for r in rlt[p:p+chunk_size]]

        async for chunk in experiments:
            results = await self._get_scans(chunk[0])

            position = 0
            while data := make_chunk(chunk[0], results, position):
                yield tuple(data)
                position += chunk_size

    async def resources(self,
                            scan: objects.Scan,
                            name: typing.Optional[str] = None,
                            action: typing.Optional[ResourceAction] = None,
                            **params: str):
        if not action:
            return await self._get_resources(scan, name)
        if not name:
            raise ValueError("Cannot perform action without resource name.")

        # I'd rather gatekeep against DELETE
        # operations as a loss of data can be
        # detrimental to production environments.
        if action is ResourceAction.DELETE:
            method = "DELETE"
        else:
            method = "POST"

        if action is not ResourceAction.REFRESH:
            url = _join_uri(self, scan.URI.lstrip("/"), "resources", name)
        else:
            url = _join_uri(self, "data", "services", "refresh", "catalog")
            resource = "/".join([
                "archive",
                "projects",
                scan.experiment.project,
                "subjects",
                scan.experiment.subject_id,
                "experiments",
                scan.experiment.id,
                "scans",
                scan.id,
                "resources",
                name])
            options = ",".join(["checksum", "delete", "append", "populateStats"])
            params.update({"resource": resource, "options": options})

        res = await self._client.request(
            method,
            url,
            timeout=self._timeouts, #type: ignore[arg-type]
            params=params)
        res.raise_for_status()

    @classmethod
    def build_client(cls, api: typing.Self):
        auth = httpx.BasicAuth(api._username, api._password)
        return httpx.AsyncClient(auth=auth)

    async def _get_resources(self, scan: objects.Scan, name: typing.Optional[str]):
        parts = scan.URI.lstrip("/"), "resources"
        if name:
            parts += name, "files" #type: ignore[assignment]

        url = _join_uri(self, *parts)
        res = await self._client.get(url,
                        timeout=self._timeouts, #type: ignore[arg-type]
                        params={"format": "json"})
        res.raise_for_status()

        ret = _parse_rest_result(res)
        if name:
            return tuple([objects.FileData.from_mapping(r) for r in ret])
        return tuple(ret)

    async def _get_scans(self, experiment: objects.Experiment) -> _MappingSeries:
        columns = _join_columns(
            "ID", "type", "series_description", "quality", "URI")
        url = _join_uri(self, experiment.URI.lstrip("/"), "scans")
        res = (await self._client.get(url,
                        follow_redirects=True,
                        timeout=self._timeouts, #type: ignore[arg-type]
                        params={"format": "json", "columns": columns}))
        res.raise_for_status()
        return _parse_rest_result(res)

    def _parse_exp_or_pjt(self, exp_or_pjt) -> _AsyncChunkGenerator[objects.Experiment]:
        if isinstance(exp_or_pjt, objects.Experiment):
            return _aiter(((exp_or_pjt,),))
        return self.get_experiments(exp_or_pjt, chunk_size=1)

    @typing.overload
    def __init__(self, hostname: str):
        ...

    @typing.overload
    def __init__(self,
                 hostname: str,
                 *,
                 username: str | None = None,
                 password: str | None = None,
                 protocol: WebProtocol | None = None,
                 port: int | None = None):
        ...

    def __init__(self,
                 hostname: str,
                 *,
                 username: str | None = None,
                 password: str | None = None,
                 protocol: WebProtocol | None = None,
                 port: int | None = None):

        self._hostname = hostname
        self._username = username or ""
        self._password = password or ""
        self._protocol = protocol or WebProtocol.HTTP
        self._port_number = port

    async def __aenter__(self):
        self._client = await self.build_client(self).__aenter__()
        return self

    async def __aexit__(self, *exc_details):
        await self._client.__aexit__(*exc_details)
        del self._client
