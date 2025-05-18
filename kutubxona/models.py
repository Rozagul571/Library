from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("Username is required"))

        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self._create_user(username, password, **extra_fields)

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        OPERATOR = "operator", "Operator"
        USER = "user", "User"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=200)
    daily_price = models.FloatField()

    def __str__(self):
        return self.title


class Order(models.Model):
    class Statuses(models.TextChoices):
        RESERVED = "reserved", "Reserved"
        TAKEN = "taken", "Taken"
        RETURNED = "returned", "Returned"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserve_time = models.DateTimeField(null=True, blank=True)
    taken_time = models.DateTimeField(null=True, blank=True)
    return_time = models.DateTimeField(null=True, blank=True)
    fine = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=Statuses.choices, default=Statuses.RESERVED)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.score}"