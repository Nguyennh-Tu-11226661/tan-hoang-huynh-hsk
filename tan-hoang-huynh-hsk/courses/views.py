from django.views.generic import DetailView, ListView

from .models import ClassSchedule, Course


class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_active=True)


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        return Course.objects.filter(is_active=True).prefetch_related("schedules")


class ScheduleListView(ListView):
    model = ClassSchedule
    template_name = "courses/schedule_list.html"
    context_object_name = "schedules"

    def get_queryset(self):
        queryset = ClassSchedule.objects.filter(is_active=True).select_related("course")
        course_slug = self.request.GET.get("khoa-hoc")
        if course_slug:
            queryset = queryset.filter(course__slug=course_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.filter(is_active=True)
        context["selected_course"] = self.request.GET.get("khoa-hoc", "")
        return context
