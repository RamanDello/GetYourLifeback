from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Basic Info"), {"fields": ("gender", "age", "height", "weight")}),
        (_("Daily Routine"), {"fields": ("sleep_hours", "job_type", "hours_sitting", "hours_standing")}),
        (
            _("Activity & Sport"),
            {
                "fields": (
                    "daily_steps",
                    "sport_types",
                    "training_frequency",
                    "training_duration",
                    "experience_level",
                    "available_equipment",
                ),
            },
        ),
        (_("Body Composition"), {"fields": ("body_fat_category",)}),
        (_("Goals & Budget"), {"fields": ("fitness_goal", "monthly_food_budget")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "fitness_goal", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
