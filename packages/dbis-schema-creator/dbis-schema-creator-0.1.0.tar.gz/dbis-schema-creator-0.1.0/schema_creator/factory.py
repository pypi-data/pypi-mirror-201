from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import sqlite3

import tempfile

from typing import Optional

from typeguard import typechecked

from erdiagram import ER, merge_er_diagrams

import schema_creator as sc


class CircularDependencyError(Exception):
    """
    Raised when a circular dependency is detected.
    """

    pass


class DependencyNotPresentError(Exception):
    """
    Raised when a dependency is not present.
    """

    pass


class SchemaFactory:
    """
    Factory for creating schemas
    """

    @typechecked
    def __init__(self, tables: set[sc.SchemaCreatorDeclarativeMeta] = set()) -> None:
        """
        Initializes a SchemaFactory object.

        Parameters
        ----------
        tables : set[Table]
            The tables to create.
        """
        if tables is None or len(tables) == 0:
            raise ValueError("No tables specified.")

        self.tables = tables

        # Create dependency graph
        self.dependency_graph = build_dependency_graph(self.tables)

        # Create a temporary database file
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix=".db")

        # Create the database engine
        self.engine = create_engine(f"sqlite:///{self.temp_db_file.name}")

        # Create the database tables
        sc.Base.metadata.create_all(
            self.engine, tables=[table.__table__ for table in self.tables]
        )

    @typechecked
    def populate(self, seed: Optional[int] = None) -> None:
        """
        Populates the tables with data.

        Parameters
        ----------
        seed : Optional[int], optional
            The seed to use for the random number generator, by default None
        """
        session = Session(bind=self.engine)

        # Populate tables if their dependencies have been populated
        assert len(self.dependency_graph) > 0
        while len(self.dependency_graph) > 0:
            len_before = len(self.dependency_graph)
            populated_a_table = False
            for table in self.dependency_graph.copy():
                if len(self.dependency_graph[table]) == 0:
                    table.populate(session)
                    self.dependency_graph = remove_dependency(
                        self.dependency_graph, table
                    )
                    populated_a_table = True
                    break
            len_after = len(self.dependency_graph)

            if not populated_a_table:
                assert len_before == len_after
                raise CircularDependencyError(
                    "Circular dependency detected. Cannot populate tables."
                )
            else:
                assert len_before > len_after
        assert len(self.dependency_graph) == 0

        session.commit()

    @typechecked
    def to_er_diagram(self) -> ER:
        """
        Draw the ER diagram for the database.

        Returns
        -------
        ER
            The ER diagram.
        """
        graph = ER()

        for table in self.tables:
            sub_graph = table.to_er_diagram()
            graph = merge_er_diagrams(graph, sub_graph)
        return graph

    @typechecked
    def to_sql(self) -> str:
        """
        Returns the SQL schema for the database.

        Returns
        -------
        str
            The SQL schema.
        """
        con = sqlite3.connect(self.temp_db_file.name)
        schema = ""
        for line in con.iterdump():
            schema += line + "\n"
        con.close()
        return schema


@typechecked
def build_dependency_graph(
    tables: set[sc.SchemaCreatorDeclarativeMeta] = set(),
) -> dict[sc.SchemaCreatorDeclarativeMeta, set[sc.SchemaCreatorDeclarativeMeta]]:
    """
    Builds a dependency graph for the tables.

    Returns
    -------
    dict[SchemaCreatorDeclarativeMeta, set[SchemaCreatorDeclarativeMeta]]
        The dependency graph.
    """
    dependency_graph = dict()

    for table in tables:
        dependency_graph[table] = table.dependencies

    # Assert that each dependency is a key
    for table in dependency_graph:
        for dependency in dependency_graph[table]:
            if dependency not in dependency_graph:
                raise DependencyNotPresentError(
                    f"Dependency {dependency.__name__} of table {table.__name__} is not present."
                )

    return dependency_graph


@typechecked
def remove_dependency(
    graph: dict[sc.SchemaCreatorDeclarativeMeta, set[sc.SchemaCreatorDeclarativeMeta]],
    table: sc.SchemaCreatorDeclarativeMeta,
) -> dict[sc.SchemaCreatorDeclarativeMeta, set[sc.SchemaCreatorDeclarativeMeta]]:
    """
    Removes a table from the dependency graph.

    Parameters
    ----------
    graph : dict[SchemaCreatorDeclarativeMeta, set[SchemaCreatorDeclarativeMeta]]
        The dependency graph.
    table : SchemaCreatorDeclarativeMeta
        The table to remove.

    Returns
    -------
    dict[SchemaCreatorDeclarativeMeta, set[SchemaCreatorDeclarativeMeta]]
        The updated dependency graph.
    """
    # Make a deep copy of the graph
    g = dict()
    for t in graph:
        g[t] = graph[t].copy()

    # Remove the table from the graph
    g.pop(table)

    # Remove the table from the dependencies of the other tables
    for t in g:
        g[t].discard(table)

    return g
