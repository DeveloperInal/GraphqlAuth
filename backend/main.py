from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry import Schema
from controller.auth.route_schema import AuthMutation, AuthQuery

auth_schema = Schema(query=AuthQuery, mutation=AuthMutation)

auth_app = GraphQLRouter(schema=auth_schema, graphql_ide="apollo-sandbox")
app = FastAPI()
app.include_router(auth_app, prefix='/auth')

if __name__ == '__main__':
     import uvicorn
     if __name__ == "__main__":
          uvicorn.run(
               "main:app",
               host="0.0.0.0",
               port=8000,
               reload=True,
