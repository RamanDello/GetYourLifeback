from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from get_your_life_back.users.forms import BodyFatCategoryForm
from get_your_life_back.users.forms import OnboardingStep1Form
from get_your_life_back.users.models import User

if TYPE_CHECKING:
    from django.http import HttpResponse
    from django.db.models import QuerySet


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class OnboardingStep1View(LoginRequiredMixin, UpdateView):
    model = User
    form_class = OnboardingStep1Form
    template_name = "users/onboarding_step1.html"

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user

    def form_valid(self, form: OnboardingStep1Form) -> HttpResponse:
        self.request.session["onboarding_gender"] = form.cleaned_data["gender"]
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("users:onboarding-body-fat")


onboarding_step1_view = OnboardingStep1View.as_view()


class BodyFatSelectView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = BodyFatCategoryForm
    template_name = "users/onboarding_body_fat.html"

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user

    def get_context_data(self, **kwargs: object) -> dict:
        context = super().get_context_data(**kwargs)
        gender = self.request.session.get("onboarding_gender", self.request.user.gender)
        context["is_female"] = gender == User.Gender.FEMALE
        return context

    def get_success_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


body_fat_select_view = BodyFatSelectView.as_view()
