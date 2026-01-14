from django.contrib import admin
from .models import PhoneRange

@admin.register(PhoneRange)
class PhoneRangeAdmin(admin.ModelAdmin):
    list_display = ('code', 'startRange', 'endRange', 'operator', 'region', 'inn')
    list_filter = ('operator', 'region')
    search_fields = ('code', 'operator', 'region', 'inn')
    readonly_fields = ('dateUpdate',)

    fieldsets = (
    ('Диапазон номеров', {
        'fields':('code', 'startRange', 'endRange', 'capacity')
    }),
    ('Информация об операторе', {
        'fields':('operator', 'region', 'inn')
    }),
    ('Дополнительная информация', {
        'fields': ('dateUpdate',),
        'classes': ('collapse',)
    }),
    )
