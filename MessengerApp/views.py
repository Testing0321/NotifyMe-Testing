# users/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UsersDatabase
from .serializers import UsersDatabaseSerializer

from datetime import datetime

from django.core.mail import send_mail
from django.conf import settings

from django.template.loader import render_to_string


@api_view(['GET'])
def user_list(request):
    users = UsersDatabase.objects.all()
    serializer = UsersDatabaseSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_create(request, name, date, username=None, note=None):
    data = {
        'Name': name,
        'username': username,
        'Date': date,
        'Note': note
    }
    serializer = UsersDatabaseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = UsersDatabase.objects.get(pk=pk)
    except UsersDatabase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UsersDatabaseSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def user_update(request, pk, name, date, username=None, note=None):
    try:
        user = UsersDatabase.objects.get(pk=pk)
    except UsersDatabase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {
        'Name': name,
        'username': username,
        'Date': date,
        'Note': note
    }
    serializer = UsersDatabaseSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_partial_update(request, pk, name=None, date=None, username=None, note=None):
    try:
        user = UsersDatabase.objects.get(pk=pk)
    except UsersDatabase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Only update fields provided in the URL
    data = {}
    if name:
        data['Name'] = name
    if date:
        data['Date'] = date
    if username:
        data['username'] = username
    if note:
        data['Note'] = note

    serializer = UsersDatabaseSerializer(user, data=data, partial=True)  # Use partial=True for PATCH-like behavior
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_delete(request, pk):
    try:
        user = UsersDatabase.objects.get(pk=pk)
    except UsersDatabase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_filter_by_date(request):
    # Get the current date and month
    current_date = datetime.now().date()
    current_month = current_date.month
    current_day = current_date.day
    
    # Filter UsersDatabase objects matching the current date and month (ignoring year)
    users = UsersDatabase.objects.filter(Date__month=current_month, Date__day=current_day)
    
    if not users.exists():
        return Response({"detail": "No users found for today's date and month."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsersDatabaseSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def user_filter_and_send_email(request):
    # Get the current date and month
    current_date = datetime.now().date()
    current_month = current_date.month
    current_day = current_date.day
    
    # Filter UsersDatabase objects matching the current date and month (ignoring year)
    users = UsersDatabase.objects.filter(Date__month=current_month, Date__day=current_day)
    
    if not users.exists():
        return Response({"detail": "No users found for today's date and month."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the filtered data
    serializer = UsersDatabaseSerializer(users, many=True)
    user_data = serializer.data

    # Prepare the email content
    subject = 'Daily User Data Report'
    recipient_email = 'mailtesting0321@gmail.com'  # Replace with the client's email address

    # Render the HTML template with user data
    html_message = render_to_string('email_template.html', {'users': user_data, 'date': current_date})

    # Send the email
    try:
        send_mail(
            subject,
            None,  # No plain text message
            settings.EMAIL_HOST_USER,
            [recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        return Response({"detail": "Users found and email sent successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": f"Error sending email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)