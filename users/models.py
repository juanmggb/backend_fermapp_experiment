"""
Database user models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise (ValueError("User must have an email"))
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    # Labnoratory director info is already here
    ROLES = (
        ("Lab Director", "Lab Director"),
        ("Student Researcher", "Student Researcher"),
    )

    role = models.CharField(max_length=200, choices=ROLES, default="Student Researcher")

    image = models.ImageField(upload_to="images/members", null=True, blank=True)

    laboratory = models.ForeignKey(
        "Laboratory",
        on_delete=models.SET_NULL,
        blank=True,  # Laboratory is optional so we can create a Lab Director before the laboratory is created
        null=True,
        related_name="members",
    )

    # laboratory_name = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email + " - " + self.role


class Laboratory(models.Model):
    laboratory_name = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    description = models.TextField()
    director = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="laboratories"
    )
    email = models.EmailField(max_length=100)

    phone_number = models.CharField(max_length=50)

    created_at = models.DateField(auto_now_add=True, null=True)

    # Probably more metada here

    class Meta:
        verbose_name_plural = "Laboratories"

    def __str__(self):
        return self.laboratory_name

    # Session Management: Allow users to see all active sessions and have the ability to log out from other devices. This is a good security measure to consider.

    # When registering a laboratory it is necessary to add a directory
    # If you try to delete a User instance that is set as a director of any Laboratory, Django will raise a ProtectedError. This means that as long as a user is assigned as a director to any laboratory, that user cannot be deleted from the database.
    # the director's record cannot be removed without first reassigning or deleting the laboratory.
