from django.contrib import admin

from .models import Company, KBEntry, QueryLog


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company_name",
        "role",
        "user",
        "created_at",
    )

    search_fields = (
        "company_name",
        "user__username",
    )

    list_filter = (
        "role",
    )


@admin.register(KBEntry)
class KBEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "category",
        "created_at",
    )

    search_fields = (
        "question",
        "answer",
    )

    list_filter = (
        "category",
    )


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company",
        "search_term",
        "results_count",
        "queried_at",
    )

    search_fields = (
        "company__company_name",
        "search_term",
    )