from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from config.admin_site import configure_admin_site
from core.sitemaps import BlogSitemap, CourseSitemap, StaticViewSitemap


configure_admin_site()
admin.site.site_header = "Tân Hoàng Huynh HSK"
admin.site.site_title = "Quản trị Tân Hoàng Huynh"
admin.site.index_title = "Quản lý nội dung và tuyển sinh"

sitemaps = {
    "pages": StaticViewSitemap,
    "courses": CourseSitemap,
    "blog": BlogSitemap,
}

urlpatterns = [
    path("quan-tri/", admin.site.urls),
    path("", include("core.urls")),
    path("khoa-hoc/", include("courses.urls")),
    path("", include("admissions.urls")),
    path("", include("content.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG and settings.MEDIA_STORAGE == "local":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.MEDIA_STORAGE == "local":
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    ]
