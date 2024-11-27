from django.shortcuts import render, redirect
from django.db import connection
from .models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def authenticate_user(request, username=None, password=None):
    with connection.cursor() as cursor:
        
        que = f"SELECT password FROM polls_user WHERE username = '{username}'" # Vunrable to SQL Injection example user' OR 'user'='user
        cursor.execute(que)
        rows = cursor.fetchall()
        #rows = User.objects.raw("SELECT id, password FROM polls_user WHERE username = %s", [username])
        for row in rows:
            user = row
            if user:
                if user[0]==password: # Assuming passwords are stored in plain text (not recommended)
                    return True
    return None

def index(request):
    users = User.objects.all()
    return render(request, 'pages/index.html', {'users': users})

def addMessages(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content and request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user.message = message_content
            user.save()
    return redirect('index')

def clearMessages(request):
    if request.user.is_authenticated and request.user.is_admin:
        users = User.objects.all()
        for user in users:
            user.message = ""
            user.save()
    return redirect('index')

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

#def initialUsers():
    users = [
        {
            'username': 'user1',
            'password': make_password('password'),
            'is_admin': False,
            'message': 'Hello, I am user1.'
        },
        {
            'username': 'user2',
            'password': make_password('password'),
            'is_admin': False,
            'message': 'Hello, I am user2.'
        },
        {
            'username': 'admin',
            'password': make_password('password'),
            'is_admin': True,
            'message': 'Welcome to the admin panel.'
        }
    ]
    User.objects.bulk_create([User(**user) for user in users])
    print('Users created successfully')

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
            'password': 'password',
            'is_admin': True
        }
    ]
    User.objects.bulk_create([User(**user) for user in users])
    print('Users created successfully')