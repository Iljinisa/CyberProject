from django.shortcuts import render, redirect
from django.db import connection
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django_ratelimit.decorators import ratelimit

def authenticate_user( username=None, password=None):
    try:
        # Secure query with parameterized input
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, password, message, is_admin FROM polls_user WHERE username = %s", [username])
            row = cursor.fetchone()
        # Check the password securely
            if row and check_password(password, row[2]):  # Uses secure hashing
                return { 
                'id': row[0],
                'username': row[1],
                'message': row[3],
                'is_admin': row[4],
            }
    except Exception as e:
        print(f"Authentication error: {e}")
    return None

@csrf_protect
def index(request):
    if 'user_id' not in request.session:
        request.session.flush()
        return redirect('login')
    messages = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT message FROM polls_user")
        rows = cursor.fetchall()
        for row in rows:
            messages.append(row[0])
    request.session['messages'] = messages
    return render(request, 'pages/index.html', {'messages': messages})

@csrf_protect
@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def user_login(request):
    if User.objects.count() == 0:
        initialUsers()  # Create initial users if none exist
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate_user( username=username, password=password)
        if user:
            request.session['user_id'] = user['id']
            return redirect('index')
        else:
            return render(request, 'pages/login.html', {'error': 'Invalid credentials'})
    return render(request, 'pages/login.html')

@csrf_protect
def logout(request):
    request.session.flush()  # Clears all session data
    return redirect('login')


# This function is used to create initial users in the database where the passwords are hashed
def initialUsers():
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
            'password': make_password('admin'),
            'is_admin': True,
            'message': 'Welcome to the admin panel.'
        }
    ]
    User.objects.bulk_create([User(**user) for user in users])
    print('Users created successfully')