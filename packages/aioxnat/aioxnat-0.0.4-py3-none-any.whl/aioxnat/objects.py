import dataclasses, enum, functools, re, pathlib
import abc, typing

Ps = typing.ParamSpec("Ps")
Ta = typing.TypeVar("Ta")

GenericTypeFactory = (
    typing.Callable[[type[Ta]], Ta] |
    typing.Callable[typing.Concatenate[type[Ta], Ps], Ta])
"""
Outline of callable which produces an object of
the given type.
"""

Validator = (
    typing.Callable[[Ta], bool] |
    typing.Callable[typing.Concatenate[Ta, Ps], bool])
"""
Callable returning whether object passes
validation.
"""

@typing.overload
def validator(**params) -> Validator:
    ...


@typing.overload
def validator(vfn: Validator, /) -> Validator:
    ...


def validator(vfn: Validator | None = None, **params):
    """
    Marks some callable as a validator function.
    """

    def wrapper(vfn: Validator):

        @functools.wraps(vfn)
        def inner(*args, **kwds):
            return vfn(*args, **kwds)

        ret = functools.partial(inner, **params)
        setattr(ret, "__is_validator__", True)
        return ret

    if vfn:
        return wrapper(vfn)
    return wrapper


def isvalidator(vfn: typing.Callable) -> bool:
    """
    Whether this callable is a validator.
    """

    return (callable(vfn) and getattr(vfn, "__is_validator__", False))


def members(enumt: type[enum.StrEnum]):
    return enumt.__members__


class ScanQuality(enum.StrEnum):
    USABLE = enum.auto()
    GOOD = enum.auto()
    FAIR = enum.auto()
    QUESTIONABLE = enum.auto()
    POOR = enum.auto()
    UNUSABLE = enum.auto()
    UNDETERMINED = enum.auto()


class ScanSubType(enum.StrEnum):
    UNKNOWN = enum.auto()


class ScanTaskType(enum.StrEnum):
    UNKNOWN = enum.auto()


@typing.runtime_checkable
class ProjectObject(typing.Protocol):
    """
    An element in the heirarchy of an XNAT
    project.
    """

    __validators__: typing.Iterable[Validator[typing.Self, Ps]] = () #type: ignore[valid-type]

    @functools.cached_property
    def is_valid(self):
        """
        Whether or not this `ProjectObject` is
        valid according to it's validators.
        """

        return all([vfn(self) for vfn in self.__validators__])

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        The name associated with this object.
        """

    @abc.abstractmethod
    def into_mapping(self) -> typing.Mapping[str, str]:
        """
        Transforms this object into a mapping of
        it's values.
        """

    @classmethod
    @abc.abstractmethod
    def from_mapping(cls, mapping: typing.Mapping[str, str]) -> typing.Self:
        """
        Transforms the given mapping into a this
        `ProjectObject` type.
        """

    @classmethod
    def insert_validator(cls, vfn: Validator[typing.Self, Ps]) -> None:
        """
        Inserts a validator into this object's
        series of validators.
        """

        tmp = set(cls.__validators__)
        if vfn in tmp:
            raise ValueError("validator already included.")

        tmp.add(vfn) #type: ignore[arg-type]
        cls.__validators__ = tuple(tmp)

    @classmethod
    def remove_validator(cls, vfn: Validator[typing.Self, Ps]) -> None:
        """
        Removes a validator from the series of
        validators.
        """

        tmp = set(cls.__validators__)
        if vfn not in tmp:
            raise ValueError("validator not in validators.")

        tmp.remove(vfn) #type: ignore[arg-type]
        cls.__validators__ = tuple(tmp)

    def __init_subclass__(cls):
        # Find and 'register' validators.
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if not (attr and isvalidator(attr)):
                continue

            try:
                cls.insert_validator(attr)
            except ValueError:
                ... # validator already inserted.


class BaseExperiment(ProjectObject):
    id: str
    label: str
    project: str

    @functools.cached_property
    def session_number(self): #NOTE: might be HCP specific.
        return ("2" if re.match(r"^.*_X1$", self.label) else "1")

    @functools.cached_property
    def name(self):
        return ":".join([self.project, self.id])

    def into_mapping(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_mapping(cls, mapping: typing.Mapping[str, str]):
        parsed = dict(mapping)
        parsed["id"] = parsed.pop("xnat:subjectassessordata/id", "")
        parsed["subject_id"] = parsed.pop("subject_label", "")
        return cls(**parsed)

    @validator
    def _valid_id(self):
        return bool(re.match(r".*[a-zA-Z0-9].*", self.id))


@dataclasses.dataclass(slots=True, frozen=True)
class Experiment(BaseExperiment):
    id: str
    xsiType: str
    subject_id: str
    project: str
    label: str
    URI: str


class BaseScan(ProjectObject):
    id: str
    series_description: str
    experiment: Experiment

    __subtype_enum__: type[enum.StrEnum] = ScanSubType
    __tasktype_enum__: type[enum.StrEnum] = ScanTaskType

    @functools.cached_property
    def name(self):
        return ":".join([self.experiment.id, self.id, self.series_description])

    @functools.cached_property
    def subtype(self) -> enum.StrEnum:
        """
        Associated purpose of this scan in
        addition to the task type.
        """

        pattern = r"^.*_(%s).*$" % r"|".join(members(self.__subtype_enum__).values())
        tmp = re.findall(pattern, self.series_description)

        try:
            return self.__subtype_enum__(tmp[0])
        except IndexError:
            return self.__subtype_enum__("UNKNOWN")

    @functools.cached_property
    def task(self) -> enum.StrEnum:
        """
        Associated task or purpose for which this
        scan was taken.
        """

        pattern = r"^.*(%s).*$" % r"|".join(members(self.__tasktype_enum__).values())
        tmp = re.findall(pattern, self.series_description)

        try:
            return self.__tasktype_enum__(tmp[0])
        except IndexError:
            return self.__tasktype_enum__("UNKNOWN")

    def into_mapping(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_mapping(cls, mapping: typing.Mapping[str, str]):
        parsed = dict(mapping)
        parsed.pop("xnat_imagescandata_id", None)
        parsed["id"] = parsed.pop("ID", "")
        parsed["data_type"] = parsed.pop("type", "")
        parsed["quality"] = ScanQuality(parsed["quality"])
        return cls(**parsed)

    def set_subtypes(self, enumt: type[enum.StrEnum]):
        """
        Sets the enumerator used to identify what
        the sub type of the scan could be.
        """

        if "UNKNOWN" not in members(enumt):
            raise AttributeError("Enum type must have member 'UNKNOWN'.")
        self.__subtype_enum__ = enumt

    def set_tasktypes(self, enumt: type[enum.StrEnum]):
        """
        Sets the enumerator used to identify what
        the task type could be.
        """

        if "UNKNOWN" not in members(enumt):
            raise AttributeError("Enum type must have member 'UNKNOWN'.")
        self.__tasktype_enum__ = enumt

    @validator
    def _valid_subtype(self):
        return (self.subtype.value != "UNKNOWN")

    @validator
    def _valid_tasktype(self):
        return (self.task.value != "UNKNOWN")


@dataclasses.dataclass(slots=True, frozen=True)
class Scan(BaseScan):
    id: str
    data_type: str
    series_description: str
    quality: ScanQuality
    URI: str
    experiment: Experiment


class BaseFileData(ProjectObject):
    URI: str

    @property
    def name(self):
        return pathlib.Path(self.URI).name

    def into_mapping(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_mapping(cls, mapping: typing.Mapping[str, str]):
        parsed = dict(mapping)

        # Name attribute is unnecessary.
        parsed.pop("Name", "")

        parsed["cat_id"] = parsed.pop("cat_ID", "")
        parsed["content"] = parsed.pop("file_content", "")
        parsed["format"] = parsed.pop("file_format", "")
        parsed["size"] = parsed.pop("Size", "")
        parsed["tags"] = parsed.pop("file_tags", "")

        return cls(**parsed)


@dataclasses.dataclass(slots=True, frozen=True)
class FileData(BaseFileData):
    content: str
    size: str
    tags: str | tuple[str]
    cat_id: str
    digest: str
    collection: str
    format: str
    URI: str


ExperimentFactory = GenericTypeFactory[Experiment, Ps]
"""
Callable which produces an `Experiment` object.
"""

ScanFactory = GenericTypeFactory[Scan, Ps]
"""Callable which produces a `Scan` object."""
