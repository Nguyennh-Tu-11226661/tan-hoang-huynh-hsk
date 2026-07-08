import time

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import ConsultationRequestForm, TrialLessonBookingForm
from .models import ConsultationRequest, TrialLessonBooking
from .notifications import notify_consultation_request, notify_trial_booking


class RateLimitMixin:
    rate_limit_seconds = 60

    def form_valid(self, form):
        key = f"last_submit_{self.__class__.__name__}"
        last_submit = self.request.session.get(key, 0)
        if time.time() - last_submit < self.rate_limit_seconds:
            form.add_error(None, "Bạn vừa gửi một yêu cầu. Vui lòng chờ một phút.")
            return self.form_invalid(form)
        self.request.session[key] = time.time()
        return super().form_valid(form)


class ConsultationCreateView(RateLimitMixin, CreateView):
    model = ConsultationRequest
    form_class = ConsultationRequestForm
    template_name = "admissions/consultation_form.html"
    success_url = reverse_lazy("admissions:success")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("course", "").isdigit():
            initial["course"] = self.request.GET["course"]
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.errors:
            return response
        notify_consultation_request(self.object)
        messages.success(
            self.request,
            "Đăng ký đã được ghi nhận. Tư vấn viên sẽ gọi lại trong giờ làm việc.",
        )
        return response


class TrialLessonCreateView(RateLimitMixin, CreateView):
    model = TrialLessonBooking
    form_class = TrialLessonBookingForm
    template_name = "admissions/trial_form.html"
    success_url = reverse_lazy("admissions:success")

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.errors:
            return response
        notify_trial_booking(self.object)
        messages.success(
            self.request,
            "Đặt lịch thành công. Trung tâm sẽ liên hệ để xác nhận khung giờ.",
        )
        return response


class SubmissionSuccessView(TemplateView):
    template_name = "admissions/success.html"
