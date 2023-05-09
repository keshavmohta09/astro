from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from helpers.files import ValidateFileSize
from users.models import Profile, User
from users.serializers import UserSerializer


class UserAPI(ViewSet):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(required=False)
        password = serializers.CharField()
        confirm_password = serializers.CharField()
        aadhaar = serializers.CharField(max_length=12)
        pan_card = serializers.CharField(max_length=10)
        address = serializers.CharField()

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
            if not attrs["aadhaar"].isdigit():
                raise serializers.ValidationError("Provide valid aadhaar number.")
            return attrs

    class FileInputSerializer(serializers.Serializer):
        image = serializers.ImageField(
            validators=[
                ValidateFileSize(max_file_size=Profile.MAX_FILE_SIZE_ALLOWED),
                FileExtensionValidator(allowed_extensions=Profile.EXTENSIONS_ALLOWED),
            ]
        )

    class OutputSerializer(UserSerializer):
        message = serializers.CharField()

        class Meta:
            model = User
            fields = ("email", "first_name", "last_name", "message")

    def create(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, "registration.html")
        data = request.POST
        serializer = self.InputSerializer(data=data)
        if not serializer.is_valid():
            messages.error(request, str(serializer.errors))
            return render(request, "registration.html")
        validated_data = serializer.validated_data

        image = request.FILES
        image_serializer = self.FileInputSerializer(data=image)
        if not image_serializer.is_valid():
            messages.error(request, str(image_serializer.errors))
            return render(request, "registration.html")
        image_data = image_serializer.validated_data

        validated_data.pop("confirm_password")
        try:
            user = User.objects.create_user(
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=validated_data["password"],
                is_buyer=True,
            )
            _profile = Profile.objects.create(
                user=user,
                photo=image_data["image"],
                aadhar_card=validated_data["aadhaar"],
                pan_card=validated_data["pan_card"],
                address=validated_data["address"],
            )
        except (ValidationError, IntegrityError) as error:
            messages.error(request, str(error))
            return render(request, "registration.html")
        messages.info(request, f"Congratulations {user.full_name}, You are registered.")
        return render(request, "index.html")

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


from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render


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
        data = request.POST
        serializer = self.InputSerializer(data=data)
        if not serializer.is_valid():
            messages.error(request, serializer.errors)
            return redirect("user-login")

        validated_data = serializer.validated_data
        email = validated_data["email"]
        password = validated_data["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, "index.html")
        messages.error(request, "Invalid email or password")
        return render(request, "login.html")

    @permission_classes(IsAuthenticated)
    def logout(self, request, *args, **kwargs):
        auth_logout(request)
        return render(request, "index.html")
