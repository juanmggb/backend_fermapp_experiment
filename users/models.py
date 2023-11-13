from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Social Sign-In: Consider allowing users to sign in through existing social media or Google accounts for ease of use.

# Terms and Conditions / Privacy Policy: Ensure that users have easy access to terms and conditions, and privacy policy documents, and that they agree to them during the sign-up process.

# User Feedback: Allow users to provide feedback or report issues directly through their account portal

# Quota Management: Especially for a data-intensive application, having an admin feature to set usage quotas can help manage server loads.

# User Analytics: Provide analytics and metrics around user behavior within the app, to help admins make data-driven decisions.


class Laboratory(models.Model):
    laboratory_name = models.CharField(max_length=200)

    location = models.CharField(max_length=200)

    # A brief description of the laboratory, including its focus area or specialization.
    description = models.TextField()

    # Session Management: Allow users to see all active sessions and have the ability to log out from other devices. This is a good security measure to consider.

    director = models.ForeignKey(
        "Member", on_delete=models.SET_NULL, null=True, related_name="laboratories"
    )

    director_name = models.CharField(max_length=255, null=True)

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

    name = models.CharField(max_length=255, null=True)

    role = models.CharField(max_length=200, choices=ROLES, default="Student Researcher")

    image = models.ImageField(upload_to="images/members", null=True, blank=True)

    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        blank=True,  # Laboratory is optional so we can create a Lab Director before the laboratory is created
        null=True,
        related_name="members",
    )

    laboratory_name = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username + " - " + self.role
