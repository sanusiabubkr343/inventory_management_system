from django.contrib.auth import authenticate
from rest_framework import generics, mixins, status, viewsets, filters
from .serializers import UserListSerializer, UserSignUpSerializer, LoginUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from .tokens import create_jwt_pair_for_user


User = get_user_model()


class UserViewSets(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'role']
    search_fields = [
        'email',
        'firstname',
        'lastname',
        
    ]
    ordering_fields = [
        'created_at',
    ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]

        return super().get_permissions()

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[AllowAny],
        serializer_class=UserSignUpSerializer,
        url_path='register',
    )
    def register_user(self, request, pk=None):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[AllowAny],
        serializer_class=LoginUserSerializer,
        url_path='login',
    )
    def login(self, request, pk=None):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                tokens = create_jwt_pair_for_user(user)
                serializer.validated_data["tokens"] = tokens
                serializer.validated_data["user_data"] = UserListSerializer(instance=user).data
                response = {"message": "Login Successful", "data": serializer.data}
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(
                data={"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
