from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Product, NetworkUnit


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkUnit)
class NetworkUnitAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level_display",
        "country",
        "city",
        "supplier_link",
        "debt",
        "created_at",
    )
    list_filter = ("city", "country")
    search_fields = ("name", "country", "city", "email", "street", "house_number", "supplier__name")
    actions = [clear_debt]

    readonly_fields = ("created_at", "supplier_link", "level_display")
    raw_id_fields = ("supplier",)
    filter_horizontal = ("products",)

    ordering = ("country", "city", "name")
    list_select_related = ("supplier",)

    fields = (
        "name",
        "email",
        ("country", "city"),
        ("street", "house_number"),
        "supplier",
        "supplier_link",
        "level_display",
        "products",
        "debt",
        "created_at",
    )

    def level_display(self, obj):
        return obj.level
    level_display.short_description = "Уровень"

    def supplier_link(self, obj):
        """Кликабельная ссылка на карточку поставщика в админке."""
        if not obj.supplier:
            return "—"
        url = reverse("admin:network_networkunit_change", args=[obj.supplier.pk])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
    supplier_link.short_description = "Поставщик"
