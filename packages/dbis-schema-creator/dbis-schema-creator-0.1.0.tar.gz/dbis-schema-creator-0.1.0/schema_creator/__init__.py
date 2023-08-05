from sqlalchemy.orm import declarative_base, DeclarativeMeta
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    Date,
    DateTime,
    Time,
    Text,
    LargeBinary,
    BigInteger,
    SmallInteger,
    Unicode,
    UnicodeText,
    Interval,
    Numeric,
    PickleType,
    Enum,
    JSON,
    ARRAY,
)


class SchemaCreatorDeclarativeMeta(DeclarativeMeta):
    def __init__(cls, name, bases, d):
        # Add custom logic here
        super().__init__(name, bases, d)


Base = declarative_base(metaclass=SchemaCreatorDeclarativeMeta)

from schema_creator.table import Table
from schema_creator.factory import (
    SchemaFactory,
    CircularDependencyError,
    DependencyNotPresentError,
)
