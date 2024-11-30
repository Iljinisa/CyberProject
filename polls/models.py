from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, default='user1')
    password = models.CharField(max_length=255, blank=False, default='password123')
    message = models.TextField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_logged = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    

    
