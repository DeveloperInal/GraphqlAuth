import strawberry
from controller.auth.route import AuthUser, RegUser, HelloWorld, LogoutUser

@strawberry.type
class AuthQuery(HelloWorld):
    pass

@strawberry.type
class AuthMutation(RegUser, AuthUser, LogoutUser):
    pass