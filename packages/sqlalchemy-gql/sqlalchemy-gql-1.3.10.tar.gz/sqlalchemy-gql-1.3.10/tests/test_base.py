import uuid

from graphql_api import GraphQLAPI

# noinspection DuplicatedCode
from sqlalchemy import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy_gql.mixin import GraphQLSQLAlchemyMixin


class TestModel:

    def test_basic(self):

        Base = declarative_base()

        from sqlalchemy import Column, Integer, String

        class Person(GraphQLSQLAlchemyMixin, Base):
            __tablename__ = 'people'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            age = Column(Integer)

        ed = Person(name='ed', age=55)

        schema = GraphQLAPI()

        @schema.type(root=True)
        class Root:

            @schema.field
            def person(self) -> Person:
                return ed

        gql_query = '''
            query GetPerson {
                person {
                    name
                    age
                }
            }
        '''

        result = schema.executor().execute(gql_query)

        expected = {
            "person": {
                "name": "ed",
                "age": 55
            }
        }

        assert expected == result.data

    def test_uuid(self):

        Base = declarative_base()

        from sqlalchemy import Column, String

        class Person(GraphQLSQLAlchemyMixin, Base):
            __tablename__ = 'people'
            id = Column(
                UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
            )
            name = Column(String)

        person_id = uuid.uuid4()

        person = Person(id=person_id, name='joe')

        schema = GraphQLAPI()

        @schema.type(root=True)
        class Root:

            @schema.field
            def person(self) -> Person:
                return person

        gql_query = '''
                query GetPerson {
                    person {
                        id
                        name
                    }
                }
            '''

        result = schema.executor().execute(gql_query)
        assert person_id == uuid.UUID(result.data["person"]["id"])
