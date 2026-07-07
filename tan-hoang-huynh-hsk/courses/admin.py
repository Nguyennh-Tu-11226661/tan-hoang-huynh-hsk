from django.contrib import admin

from .models import ClassSchedule, Course


class ClassScheduleInline(admin.TabularInline):
    model = ClassSchedule
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "tuition", "is_featured", "is_active", "order")
    list_editable = ("is_featured", "is_active", "order")
    list_filter = ("level", "is_featured", "is_active")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ClassScheduleInline]


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "class_code",
        "course",
        "start_date",
        "schedule_text",
        "format",
        "seats_left",
        "is_active",
    )
    list_filter = ("format", "start_date", "is_active")
    search_fields = ("class_code", "course__title", "teacher")
