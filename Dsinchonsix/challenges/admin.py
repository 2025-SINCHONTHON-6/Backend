from django.contrib import admin
from .models import *
from django import forms
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

# --- TeaLogs: created_at(DateField, auto_now_add=True)만 수정 ---
class TeaLogsAdminForm(forms.ModelForm):
    created_at_override = forms.DateField(
        label="마신 날짜(수정용)",
        required=False,
        widget=AdminDateWidget,
        help_text="비워두면 현재값 유지"
    )

    class Meta:
        model = TeaLogs
        fields = ["tea"]  # 날짜 외엔 손대지 않도록 최소 필드만 노출

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.created_at:
            self.fields["created_at_override"].initial = self.instance.created_at


@admin.register(TeaLogs)
class TeaLogsAdmin(admin.ModelAdmin):
    form = TeaLogsAdminForm
    readonly_fields = ("created_at",)
    fields = ("tea", "created_at", "created_at_override")
    list_display = ("tea", "created_at")

    def save_model(self, request, obj, form, change):
        # 1) 먼저 저장해서 auto_now_add 적용
        super().save_model(request, obj, form, change)
        # 2) 오버라이드 값이 있으면 DB 레벨에서 강제 수정
        override = form.cleaned_data.get("created_at_override")
        if override:
            type(obj).objects.filter(pk=obj.pk).update(created_at=override)
            obj.created_at = override  # 화면 즉시 반영


# --- RecentRecommendedTea: created_at(DateTimeField, auto_now=True)만 수정 ---
class RecentRecommendedTeaAdminForm(forms.ModelForm):
    created_at_override = forms.DateTimeField(
        label="추천 시각(수정용)",
        required=False,
        widget=AdminSplitDateTime,
        help_text="비우면 auto_now로 현재 시각"
    )

    class Meta:
        model = RecentRecommendedTea
        fields = ["tea"]  # 날짜 외엔 편집 막음

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.created_at:
            self.fields["created_at_override"].initial = timezone.localtime(self.instance.created_at)


@admin.register(RecentRecommendedTea)
class RecentRecommendedTeaAdmin(admin.ModelAdmin):
    form = RecentRecommendedTeaAdminForm
    readonly_fields = ("created_at",)
    fields = ("tea", "created_at", "created_at_override")
    list_display = ("tea", "created_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # auto_now 적용
        override = form.cleaned_data.get("created_at_override")
        if override:
            # naive → aware 보정
            if timezone.is_naive(override):
                override = timezone.make_aware(override, timezone.get_current_timezone())
            type(obj).objects.filter(pk=obj.pk).update(created_at=override)
            obj.created_at = override

admin.site.register(Challenge)