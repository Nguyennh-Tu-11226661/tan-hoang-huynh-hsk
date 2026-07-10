from django.conf import settings

from .models import ContactInfo


def site_context(request):
    site_url = settings.SITE_URL.rstrip("/")
    return {
        "site_contact": ContactInfo.objects.filter(is_active=True).first(),
        "site_url": site_url,
        "canonical_url": f"{site_url}{request.path}",
    }
