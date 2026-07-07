from django.urls import path

from .views import (
    BlogDetailView,
    BlogListView,
    GalleryListView,
    TestimonialListView,
)

app_name = "content"

urlpatterns = [
    path("tin-tuc/", BlogListView.as_view(), name="blog_list"),
    path("tin-tuc/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("thanh-tich-hoc-vien/", TestimonialListView.as_view(), name="testimonials"),
    path("thu-vien/", GalleryListView.as_view(), name="gallery"),
]
