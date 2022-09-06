from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, email,  password=None):
        if not email:
          raise ValueError('User must have an email adress')

        if not username:
          raise ValueError('User must have a username')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            username = username,
        )

        user.set_password(password)
        user.save(using= self._db)
        return user

    def create_superuser(self, username, first_name, email, password):     
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            password= password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save(using= self._db)
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    mobile_number = models.CharField(max_length=10)

    #required

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj= None):
        return self.is_superuser

    def has_module_perms(self, add_label):
        return True