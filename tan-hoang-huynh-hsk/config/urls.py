from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import BlogSitemap, CourseSitemap, StaticViewSitemap


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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
