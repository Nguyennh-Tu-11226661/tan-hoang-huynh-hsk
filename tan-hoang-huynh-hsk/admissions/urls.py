from django.urls import path

from .views import (
    ConsultationCreateView,
    SubmissionSuccessView,
    TrialLessonCreateView,
)

app_name = "admissions"

urlpatterns = [
    path("dang-ky-tu-van/", ConsultationCreateView.as_view(), name="consultation"),
    path("dat-lich-hoc-thu/", TrialLessonCreateView.as_view(), name="trial"),
    path("dang-ky-thanh-cong/", SubmissionSuccessView.as_view(), name="success"),
]
