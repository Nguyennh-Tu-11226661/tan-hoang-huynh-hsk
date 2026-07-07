import time

from django import forms
from django.core import signing
from django.core.exceptions import ValidationError
from django.utils import timezone

from courses.models import Course

from .models import ConsultationRequest, TrialLessonBooking


class AntiSpamFormMixin(forms.Form):
    website = forms.CharField(
        required=False,
        label="Website",
        widget=forms.TextInput(
            attrs={"tabindex": "-1", "autocomplete": "off", "class": "honeypot"}
        ),
    )
    form_started = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial["form_started"] = signing.dumps(int(time.time()))

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise ValidationError("Không thể gửi biểu mẫu. Vui lòng thử lại.")
        try:
            started = signing.loads(cleaned.get("form_started", ""), max_age=3600)
            if time.time() - int(started) < 2:
                raise ValidationError("Bạn gửi quá nhanh. Vui lòng kiểm tra lại thông tin.")
        except signing.BadSignature:
            raise ValidationError("Phiên biểu mẫu không hợp lệ. Vui lòng tải lại trang.")
        return cleaned


class ConsultationRequestForm(AntiSpamFormMixin, forms.ModelForm):
    consent = forms.BooleanField(
        label="Tôi đồng ý để trung tâm liên hệ tư vấn về lộ trình học.",
        required=True,
    )

    class Meta:
        model = ConsultationRequest
        fields = [
            "full_name",
            "phone",
            "email",
            "course",
            "current_level",
            "preferred_time",
            "message",
        ]
        labels = {
            "full_name": "Họ và tên",
            "phone": "Số điện thoại",
            "email": "Email (không bắt buộc)",
            "course": "Khóa học quan tâm",
            "current_level": "Trình độ hiện tại",
            "preferred_time": "Thời gian thuận tiện để nghe máy",
            "message": "Điều bạn muốn được tư vấn",
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
            "phone": forms.TextInput(attrs={"inputmode": "tel"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(is_active=True)
        self.fields["course"].empty_label = "Chưa chắc – cần tư vấn lộ trình"
        for name, field in self.fields.items():
            if name not in {"consent", "website", "form_started"}:
                field.widget.attrs["class"] = "form-control"
        self.fields["course"].widget.attrs["class"] = "form-select"


class TrialLessonBookingForm(AntiSpamFormMixin, forms.ModelForm):
    consent = forms.BooleanField(
        label="Tôi đồng ý để trung tâm liên hệ xác nhận lịch.",
        required=True,
    )

    class Meta:
        model = TrialLessonBooking
        fields = [
            "full_name",
            "phone",
            "email",
            "booking_type",
            "preferred_date",
            "preferred_slot",
            "current_level",
            "goal",
        ]
        labels = {
            "full_name": "Họ và tên",
            "phone": "Số điện thoại",
            "email": "Email (không bắt buộc)",
            "booking_type": "Bạn muốn đăng ký",
            "preferred_date": "Ngày mong muốn",
            "preferred_slot": "Khung giờ",
            "current_level": "Trình độ hiện tại",
            "goal": "Mục tiêu tiếng Trung",
        }
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "goal": forms.Textarea(attrs={"rows": 3}),
            "phone": forms.TextInput(attrs={"inputmode": "tel"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferred_slot"].widget = forms.Select(
            choices=[
                ("", "Chọn khung giờ"),
                ("08:00–10:00", "08:00–10:00"),
                ("14:00–16:00", "14:00–16:00"),
                ("18:00–20:00", "18:00–20:00"),
            ]
        )
        for name, field in self.fields.items():
            if name not in {"consent", "website", "form_started"}:
                field.widget.attrs["class"] = (
                    "form-select"
                    if isinstance(field.widget, forms.Select)
                    else "form-control"
                )

    def clean_preferred_date(self):
        value = self.cleaned_data["preferred_date"]
        if value < timezone.localdate():
            raise ValidationError("Vui lòng chọn ngày từ hôm nay trở đi.")
        return value
