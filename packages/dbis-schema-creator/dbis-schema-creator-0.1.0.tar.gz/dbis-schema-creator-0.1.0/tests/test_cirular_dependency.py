from __future__ import annotations
import pytest
from schema_creator import *


class A(Table):
    a_id = Column(Integer, primary_key=True)
    b_id = Column(Integer, ForeignKey("b.b_id"))

    @staticmethod
    def populate(session, seed=None):
        session.add(A(a_id=1, b_id=1))


class B(Table):
    b_id = Column(Integer, primary_key=True)
    a_id = Column(Integer, ForeignKey("a.a_id"))

    dependencies = {A}

    @staticmethod
    def populate(session, seed=None):
        session.add(B(a_id=1, b_id=1))


A.dependencies = {B}


def test_circular_dependency():
    tables = set([A, B])
    factory = SchemaFactory(tables)
    with pytest.raises(CircularDependencyError):
        factory.populate()
