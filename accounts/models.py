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
    mobile_number = models.CharField(max_length=10, unique=True)

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

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj= None):
        return self.is_superuser

    def has_module_perms(self, add_label):
        return True

    

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile', null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=30, null=True)

    def __str__(self) :
       return self.user.first_name


class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50, blank=True)
    address=models.CharField(max_length=255)
    landmark=models.CharField(max_length=255, blank=True)
    city=models.CharField(max_length=50)
    pin_code= models.IntegerField()
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)

    date_added = models.DateTimeField(auto_now_add=True)

    # is_active is used if the user is deleted an address that is used in an order, if the dont want to see or user the address again,
    # he can delete it, but it cannot be deleted from the database. so is_active is set to false. which helps to filter address to show the user
    is_active= models.BooleanField(default=True) 

    class Meta:
      verbose_name = 'Address'
      verbose_name_plural = 'Addresses'

    def __str__(self):
      return str(self.id)

    def full_name(self):
      return self.first_name + ' ' + self.last_name

    def full_address(self):
      return self.address + ', ' + self.landmark

    def details(self):
      return self.city + ', ' + str(self.pin_code)  + ', ' + self.state  + ', ' + self.country

    def __hash__(self):
        return super().__hash__()

    def __equal__(self, other):
      if other is not None and self is not None:
        if self.user == other.user \
        and self.mobile == other.mobile \
        and self.email == other.email \
        and self.first_name == other.first_name \
        and self.last_name == other.last_name \
        and self.address == other.address \
        and self.landmark == other.landmark \
        and self.pin_code == other.pin_code \
        and self.city == other.city \
        and self.state == other.state \
        and self.country == other.country:
            return True
        else:
            return False

      else:
        return False


class Subscriber(models.Model):
    email = models.EmailField(max_length = 50, unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.email


