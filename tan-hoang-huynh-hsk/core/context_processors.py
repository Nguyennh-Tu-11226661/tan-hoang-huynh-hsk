from .models import ContactInfo


def site_context(request):
    return {"site_contact": ContactInfo.objects.filter(is_active=True).first()}
