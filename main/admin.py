from django.contrib import admin
from .models import Site, Testimony

# Register your models here.
# admin.site.register(Site)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    '''Admin View for Site'''

    list_display = ('name', 'email', 'founder')
    fieldsets = (
        ('MAIN FEATURES', {
            'fields': (
                'name', 'email', 'phone', 'address', 'founder', 'logo', 'year', 'website'
            ),
        }),
        ('WALLET ADDRESSES', {
            'fields': (
                'btc', 'eth', 'usdt'
            ),
        }),
    )


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    '''Admin View for Testimony'''

    list_display = ('name', 'title')
    list_filter = ('name',)
    search_fields = ('name', 'title')
    fieldsets = (
        ('TESTIMONY SECTION', {
            'fields': (
                'name', 'title', 'description', 'image'
            ),
        }),
    )
