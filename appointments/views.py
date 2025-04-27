from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics, permissions
from .models import Client, Appointments, Workers
from .serializers import ClientSerializer, AppointmentsSeliarizer, WorkerSerializer, RegisterSerializer, UserSerializer

# Kliens endpoints
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated]) 
def getClients(request):
    if request.method == 'GET':
        osszes = Client.objects.all().order_by('nev')
        serialized = ClientSerializer(osszes, many=True)
        return Response(serialized.data)

    elif request.method == 'POST':
        print('Incomping POST data:', request.data)
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            print('Validated data:', serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])  
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data)
        print('Data got from frontend:', request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_200_OK)

# Időpont endpoints
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])  
def appointment_list(request):
    if request.method == 'GET':
        appointments = Appointments.objects.all().order_by('-date_time')
        serializer = AppointmentsSeliarizer(appointments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AppointmentsSeliarizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# idopontok
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])  
def appointent_detail(request, pk):
    try:
        appointment = Appointments.objects.get(pk=pk)
    except Appointments.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentsSeliarizer(appointment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AppointmentsSeliarizer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_200_OK)

# Extras
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  
def upcoming_appointments(request):
    appointments = Appointments.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    serializer = AppointmentsSeliarizer(appointments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])  
def worker_list(request):
    if request.method == 'GET':
        osszes = Workers.objects.all().order_by('nev')
        serialized = WorkerSerializer(osszes, many=True)
        return Response(serialized.data)
    elif request.method == 'PUT':
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user_serializer = UserSerializer(request.user)
    try:
        worker = Workers.objects.get(user=request.user)
        worker_serializer = WorkerSerializer(worker)
        print(worker_serializer)
        data = {
            'user': user_serializer.data,
            'worker': worker_serializer.data
        }
    except:
        data = {
            'user': user_serializer.data,
            'worker': None,
        }
    return Response(data, status=status.HTTP_200_OK)