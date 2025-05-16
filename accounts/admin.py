from django.contrib import admin
from .models import account

class accountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'created_at')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'created_at')
    list_per_page = 10
    list_editable = ('role',)
    list_display_links = ('username', 'email')
    list_max_show_all = 100

# Register your models here.
admin.site.register(account, accountAdmin)
