from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declared_attr

from typing import Optional

from typeguard import typechecked

from erdiagram import ER

import schema_creator as sc


class Table(sc.Base):
    """
    A table in the database.
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    dependencies = set()

    @typechecked
    @staticmethod
    def populate(session: Session, seed: Optional[int] = None) -> None:
        """
        Populates the table with data.

        Parameters
        ----------
        session : Session
            The session to use to populate the table.
        seed : Optional[int], optional
            The seed to use for the random number generator, by default None
        """
        pass

    @typechecked
    @staticmethod
    def to_er_diagram() -> ER:
        """
        Draw the ER diagram for the database.
        Returns
        -------
        ER
            The ER diagram. (See dbis-er-diagram package)
        """
        return ER()
