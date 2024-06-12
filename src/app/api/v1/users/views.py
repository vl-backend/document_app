from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=["authentication"],
        operation_summary="Register user",
        request_body=UserSerializer(),
        responses={
            status.HTTP_201_CREATED: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
        )
        user.set_password(serializer.initial_data["password"])
        user.save()

        response_serializer = UserSerializer(
            user, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
