<<<<<<< HEAD
import strawberry
from controller.auth.route import AuthUser, RegUser, HelloWorld, LogoutUser

@strawberry.type
class AuthQuery(HelloWorld):
    pass

@strawberry.type
class AuthMutation(RegUser, AuthUser, LogoutUser):
=======
import strawberry
from controller.auth.route import AuthUser, RegUser, HelloWorld, LogoutUser

@strawberry.type
class AuthQuery(HelloWorld):
    pass

@strawberry.type
class AuthMutation(RegUser, AuthUser, LogoutUser):
>>>>>>> d8a3317a0a70d13af2213931a89ea36727542756
    pass