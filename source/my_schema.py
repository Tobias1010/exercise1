import sqlite3
import strawberry
from enum import Enum
import typing
import source.my_database


@strawberry.enum
class States(Enum):
    NSW = strawberry.enum_value('New South Wales')
    VIC = strawberry.enum_value('Victoria')
    QLD = strawberry.enum_value('Queensland')
    SA = strawberry.enum_value('South Australia')
    WA = strawberry.enum_value('Western Australia')
    NT = strawberry.enum_value('Northern Territories')
    ACT = strawberry.enum_value('Capital Territories')
    TAS = strawberry.enum_value('Tasmania', deprecation_reason='Only mainland allowed')


@strawberry.type
class Address:
    number: int
    street: str
    city: str
    state: States


@strawberry.type
class Person:
    email: str
    name: str
    address: Address


@strawberry.type
class PersonError:
    name: str
    email: str
    message: str


# Create a Union type to represent the 2 results from the mutation. This is useful to handle expected errors
Response = strawberry.union(
    "AddPersonResponse", [Person, PersonError]
)


def get_people() -> [Person]:
    with source.my_database.DB() as db:
        res = db.get_all_data()
    return [
        Person(name=r[0], email=r[1], address=Address(street=r[2], number=r[3], city=r[4], state=r[5])) for r in res
    ]


def get_person(email: str) -> Person:
    with source.my_database.DB() as db:
        r = db.get_person(email)
    return Person(name=r[0], email=r[1], address=Address(street=r[2], number=r[3], city=r[4], state=r[5]))


@strawberry.type
class Query:
    """List of queries available on graphql:
         - Query all data in the database (get_people)
         - Query single object from database (get_person)
    """
    people: typing.List[Person] = strawberry.field(resolver=get_people)
    person: Person = strawberry.field(resolver=get_person)


@strawberry.type
class Mutation:
    """List of mutation available on graphql:
          - add new person into the database (add_person)
          - delete person from database (remove_person)
    """
    @strawberry.mutation
    def add_person(self, email: str, name: str, street: str, number: int, city: str, state: str) -> Response:
        print(f"Adding {name}; email: {email}")
        with source.my_database.DB() as db:
            res = db.insert_person(name, email, street, number, city, state)
        if res == 'success':
            return Person(name=name, email=email, address=Address(street=street, number=number, city=city,
                                                                  state=state))
        else:
            return PersonError(name=name, email=email, message=str(res))

    @strawberry.mutation
    def remove_person(self, email: str) -> Person:
        with source.my_database.DB() as db:
            r = db.get_person(email)
            db.remove_person(email)
        print(f"Removing {r[0]}; email: {email}")
        return Person(name=r[0], email=r[1], address=Address(street=r[2], number=r[3], city=r[4], state=r[5]))
