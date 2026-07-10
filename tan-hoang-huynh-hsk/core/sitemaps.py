from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from content.models import BlogPost
from courses.models import Course


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "courses:list",
            "courses:schedule",
            "admissions:consultation",
            "admissions:trial",
            "content:testimonials",
            "content:gallery",
            "content:blog_list",
            "core:faq",
            "core:contact",
            "core:privacy",
        ]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_active=True)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
