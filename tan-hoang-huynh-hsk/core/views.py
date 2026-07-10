from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView

from admissions.forms import ConsultationRequestForm
from content.models import BlogPost, Testimonial
from courses.models import ClassSchedule, Course

from .models import Banner, ContactInfo, FAQ


def robots_txt(request):
    sitemap_url = f"{settings.SITE_URL.rstrip('/')}/sitemap.xml"
    return HttpResponse(
        f"User-agent: *\nAllow: /\nDisallow: /quan-tri/\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def google_site_verification(request):
    return HttpResponse(
        "google-site-verification: google8527b34d53db3d23.html",
        content_type="text/plain",
    )


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_banners = Banner.objects.filter(is_active=True)
        context.update(
            {
                "banner": active_banners.first(),
                "featured_courses": Course.objects.filter(is_active=True, is_featured=True)[:6],
                "upcoming_schedules": ClassSchedule.objects.filter(
                    is_active=True
                ).select_related("course")[:4],
                "testimonials": Testimonial.objects.filter(is_active=True, is_featured=True)[:6],
                "latest_posts": BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)[:3],
                "consultation_form": ConsultationRequestForm(),
            }
        )
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class FAQView(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = FAQ.objects.filter(is_active=True)
        return context


class ContactView(TemplateView):
    template_name = "core/contact.html"


class PrivacyPolicyView(TemplateView):
    template_name = "core/privacy_policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = ContactInfo.objects.filter(is_active=True).first()
        return context
