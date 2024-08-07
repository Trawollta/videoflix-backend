from django.contrib import admin
from .models import Video, Category

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_at', 'category')  # Zeigt die Kategorie im Admin-Bereich an
    search_fields = ('title',)

    def has_add_permission(self, request):
        return request.user.is_superuser  # Nur Superuser dürfen Videos hinzufügen

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
