from django.shortcuts import render, redirect
from django.db import connection
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def authenticate_user(request, username=None, password=None):
    with connection.cursor() as cursor:
        que = f"SELECT password FROM polls_user WHERE username = '{username}'" # Vunrable to SQL Injection example user' OR 'user'='user
        cursor.execute(que)
        rows = cursor.fetchall()
        for row in rows:
            user = row
            if user:
                if user[0]==password: # When stored in plaintext
                    return True
    return None

def index(request):
    users = User.objects.all()
    return render(request, 'pages/index.html', {'users': users})

def logout(request):
    return redirect('login')

@csrf_exempt
def user_login(request):
    if User.objects.count() == 0:
        initialUsers()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate_user(request, username=username, password=password)
        if user is not None:
            return redirect('index')
    return render(request, 'pages/login.html')


# This function is used to create initial users in the database where the passwords are stored in plain text
def initialUsers():
    users = [
        {
            'username': 'user1',
            'password': 'password'
        },
        {
            'username': 'user2',
            'password': 'password'
        },
        {
            'username': 'admin',
            'password': 'admin',
            'is_admin': True
        }
    ]
    User.objects.bulk_create([User(**user) for user in users])
    print('Users created successfully')