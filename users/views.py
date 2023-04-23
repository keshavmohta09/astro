from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import User
from users.serializers import UserSerializer


class UserAPI(ViewSet):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(required=False)
        password = serializers.CharField()
        confirm_password = serializers.CharField()

        def validate(self, attrs):
            if bool(attrs.get("password")) ^ bool(attrs.get("confirm_password")):
                raise serializers.ValidationError(
                    "Confirm password is required when password is provided."
                )

            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError(
                    "Password and confirm password do not match."
                )
            validate_password(attrs["password"])
            return attrs

    class OutputSerializer(UserSerializer):
        message = serializers.CharField()

        class Meta:
            model = User
            fields = ("email", "first_name", "last_name", "message")

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.InputSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        validated_data.pop("confirm_password")
        try:
            user = User.objects.create_user(**validated_data)
        except (ValidationError, IntegrityError) as error:
            return Response(str(error), status=400)
        user.message = "Congratulations, You are registered."
        return Response(self.OutputSerializer(instance=user).data, status=201)

    def update(self, request, *args, **kwargs):
        data = request.data
        if "email" in data:
            return Response(
                data="To update the email you have to send a update request at care@bidders.com",
                status=400,
            )
        serializer = self.InputSerializer(data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        validated_data.pop("confirm_password")
        user = request.user
        for field, value in validated_data.items():
            setattr(user, field, value)
        try:
            user.save()
        except (ValidationError, IntegrityError) as error:
            return Response(str(error), status=400)
        user.message = "User updated successfully."

        return Response(self.OutputSerializer(instance=user).data, status=201)


from django.shortcuts import render


class UserAuthenticationAPI(ViewSet):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    class OutputSerializer(UserSerializer):
        class Meta:
            model = User
            fields = ("email", "first_name", "last_name")

    def login(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, "login.html")
        data = request.POST.data
        serializer = self.InputSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        email = validated_data["email"]
        password = validated_data["password"]
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response("User not found. Please register yourself before login.")
        token, _created = Token.objects.get_or_create(user=user)
        response = {
            "token": token.key,
            "payload": self.OutputSerializer(instance=user).data,
        }
        return Response(response, status=200)

    @permission_classes(IsAuthenticated)
    def logout(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()

        return Response(status=204)
