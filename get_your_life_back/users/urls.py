from django.urls import path

from .views import body_fat_select_view
from .views import onboarding_step1_view
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("onboarding/step-1/", view=onboarding_step1_view, name="onboarding-step1"),
    path("onboarding/body-fat/", view=body_fat_select_view, name="onboarding-body-fat"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
