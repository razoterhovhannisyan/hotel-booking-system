from rest_framework import serializers
from . import models
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation



class RegiserUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didnt match"})
        return attrs


    def create(self, validated_data):
        user = models.User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=64, write_only=True, required=True)
    new_password = serializers.CharField(max_length=64, write_only=True, required=True)
    new_password_confirmation = serializers.CharField(
        max_length=64, write_only=True, required=True
    )

    def validate_old_password(self, old_password):
        if self.instance.check_password(old_password):
            return old_password
        raise serializers.ValidationError('Old password is incorrect')

    def validate(self, data):
        if data.get("new_password") != data.get("new_password_confirmation"):
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(data.get("new_password"), self.instance)
        return data

    def save(self):
        user = self.instance
        user.set_password(self.validated_data.get("new_password"))
        user.save()
        return user
