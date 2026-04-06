
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import DecimalField
from django.db.models import EmailField
from django.db.models import FloatField
from django.db.models import PositiveIntegerField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for get-your-life-back.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")

    class JobType(models.TextChoices):
        SEDENTARY = "sedentary", _("Sedentary / Office")
        LIGHTLY_ACTIVE = "lightly_active", _("Lightly Active / Standing")
        ACTIVE = "active", _("Active / Manual Labor")
        HEAVY = "heavy", _("Heavy Manual Labor")

    class DailySteps(models.TextChoices):
        UNDER_4K = "under_4k", _("<4,000")
        FROM_4K_TO_7K = "4k_7k", _("4,000–7,000")
        FROM_7K_TO_10K = "7k_10k", _("7,000–10,000")
        FROM_10K_TO_13K = "10k_13k", _("10,000–13,000")
        OVER_13K = "over_13k", _("13,000+")

    class ExperienceLevel(models.TextChoices):
        BEGINNER = "beginner", _("Beginner")
        INTERMEDIATE = "intermediate", _("Intermediate")
        PRO = "pro", _("Pro")

    class AvailableEquipment(models.TextChoices):
        FULL_GYM = "full_gym", _("Full Gym")
        HOME_GYM = "home_gym", _("Home Gym")
        NO_EQUIPMENT = "none", _("No Equipment")

    class FitnessGoal(models.TextChoices):
        WEIGHT_LOSS = "weight_loss", _("Weight Loss")
        BUILD_MUSCLE = "build_muscle", _("Build Muscle / Maintain")
        BULK_AND_CUT = "bulk_and_cut", _("Bulk & Cut")
        STAY_FIT = "stay_fit", _("Stay Fit")

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    # --- Basic Info ---
    gender = CharField(max_length=10, choices=Gender.choices, blank=True)
    age = PositiveIntegerField(null=True, blank=True)
    height = FloatField(null=True, blank=True, help_text=_("Height in cm"))
    weight = FloatField(null=True, blank=True, help_text=_("Weight in kg"))

    # --- Daily Routine ---
    sleep_hours = PositiveIntegerField(null=True, blank=True)
    job_type = CharField(max_length=20, choices=JobType.choices, blank=True)
    hours_sitting = PositiveIntegerField(null=True, blank=True)
    hours_standing = PositiveIntegerField(null=True, blank=True)

    # --- Activity & Sport ---
    daily_steps = CharField(max_length=10, choices=DailySteps.choices, blank=True)
    sport_types = CharField(
        max_length=255,
        blank=True,
        help_text=_("Comma-separated: Ball Sports, Gym/Strength, Calisthenics, Endurance, Martial Arts"),
    )
    training_frequency = PositiveIntegerField(
        null=True, blank=True, help_text=_("Days per week"),
    )
    training_duration = PositiveIntegerField(
        null=True, blank=True, help_text=_("Minutes per session"),
    )
    experience_level = CharField(
        max_length=15, choices=ExperienceLevel.choices, blank=True,
    )
    available_equipment = CharField(
        max_length=15, choices=AvailableEquipment.choices, blank=True,
    )

    # --- Goals & Budget ---
    fitness_goal = CharField(max_length=20, choices=FitnessGoal.choices, blank=True)
    monthly_food_budget = DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
