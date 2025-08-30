from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # Campo de contraseña solo para escritura
    password = serializers.CharField(write_only=True, required=True)
    # Campo de confirmación de contraseña solo para escritura
    password2 = serializers.CharField(write_only=True, required=True)
    # Campo de usuario (auto creación)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password2",
            "is_active",
            "sucursal",
            "puesto",
            "salario",
        ]
        # Campos de solo lectura
        read_only_fields = ["id"]

    def validate(self, attrs):
        # Validar que las contraseñas coincidan
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden"}
            )
        return attrs

    def create(self, validated_data):
        # Eliminar password2 ya que no es un campo del modelo
        validated_data.pop("password2", None)
        # Encriptar la contraseña
        validated_data["password"] = make_password(validated_data.get("password"))
        # Crear nombre de usuario (usuarios de correo, sin el después del @)
        validated_data["username"] = validated_data["email"].split("@")[0]

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Eliminar password2 ya que no es un campo del modelo
        validated_data.pop("password2", None)
        # Si se incluye contraseña, encriptarla
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data.get("password"))
        return super().update(instance, validated_data)
