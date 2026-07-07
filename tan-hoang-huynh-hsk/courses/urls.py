from django.urls import path

from .views import CourseDetailView, CourseListView, ScheduleListView

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="list"),
    path("lich-khai-giang/", ScheduleListView.as_view(), name="schedule"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="detail"),
]
