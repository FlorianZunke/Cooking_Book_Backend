from rest_framework.views import APIView
from rest_framework.permissions import AllowAny



class RegisterView(APIView):
    permissions_class=[AllowAny]

class LoginView(APIView):
    pass