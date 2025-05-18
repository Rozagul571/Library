from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        OPERATOR = "operator", "Operator"
        USER = "user", "User"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=200)
    daily_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.score}"