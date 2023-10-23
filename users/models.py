from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Laboratory(models.Model):
    laboratory_name = models.CharField(max_length=200, unique=True)

    location = models.CharField(max_length=200)

    # A brief description of the laboratory, including its focus area or specialization.
    description = models.TextField()

    director = models.ForeignKey(
        "Member", on_delete=models.SET_NULL, null=True, related_name="laboratories"
    )

    email = models.EmailField(max_length=100)

    phone_number = models.CharField(max_length=50)

    created_at = models.DateField(auto_now_add=True, null=True)

    # laboratory_director = models.ForeignKey("Memeber", on_delete=models.SET_NULL, null=True)

    # Probably more metada here

    class Meta:
        verbose_name_plural = "Laboratories"

    def __str__(self):
        return self.laboratory_name


class Member(models.Model):
    # Labnoratory director info is already here
    ROLES = (
        ("Lab Director", "Lab Director"),
        ("Student Researcher", "Student Researcher"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")

    role = models.CharField(max_length=200, choices=ROLES, default="Student Researcher")

    image = models.ImageField(upload_to="images/members", null=True, blank=True)

    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="members",
    )

    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username + " - " + self.role
