from rest_framework import serializers
from .models import Client, Appointments, Workers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()
class ClientSerializer(serializers.ModelSerializer):
    masseur = serializers.PrimaryKeyRelatedField(queryset=Workers.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Client
        fields = ['id', 'nev', 'email', 'phone', 'masseur', ]
        depth = 2

class AppointmentsSeliarizer(serializers.ModelSerializer):
    nev = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True, source='nev')
    class Meta:
        model = Appointments
        fields = ['id', 'nev', 'client_id', 'notes', 'status', 'date_time']
        depth= 1


class WorkerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Workers
        fields = ['id', 'nev', 'user']

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
