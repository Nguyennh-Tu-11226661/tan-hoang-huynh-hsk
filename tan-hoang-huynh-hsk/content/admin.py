from django.contrib import admin

from .models import BlogPost, GalleryImage, Testimonial


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name", "status", "published_at", "updated_at")
    list_filter = ("status", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("student_name", "course_name", "score", "rating", "is_featured", "is_active")
    list_editable = ("is_featured", "is_active")
    search_fields = ("student_name", "course_name", "content")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "event_date", "order", "is_active")
    list_filter = ("media_type", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "caption")
