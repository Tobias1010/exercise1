import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from source.my_schema import Query, Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(
    schema=schema,                  # schema created by strawberry
    graphiql=True,                  # enable graphQL interface
    allow_queries_via_get=True,
)
app = FastAPI()


@app.get('/')
def read_form():
    return 'page not available. Browse to /graphql'


app.add_route("/graphql", graphql_app)

