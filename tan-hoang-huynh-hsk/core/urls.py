from django.urls import path

from .views import (
    AboutView,
    ContactView,
    FAQView,
    HomeView,
    PrivacyPolicyView,
    google_site_verification,
    robots_txt,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("gioi-thieu/", AboutView.as_view(), name="about"),
    path("cau-hoi-thuong-gap/", FAQView.as_view(), name="faq"),
    path("lien-he/", ContactView.as_view(), name="contact"),
    path("chinh-sach-bao-mat/", PrivacyPolicyView.as_view(), name="privacy"),
    path("robots.txt", robots_txt, name="robots"),
    path(
        "google8527b34d53db3d23.html",
        google_site_verification,
        name="google_site_verification",
    ),
]
