from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient,
    RecipeTag, Favorite, ShoppingCart
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    ordering = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1
    autocomplete_fields = ('tag',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'cooking_time',
        'created_at', 'favorites_count', 'image_preview'
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags', 'created_at')
    autocomplete_fields = ('author',)
    inlines = (RecipeIngredientInline, RecipeTagInline)
    readonly_fields = ('favorites_count', 'image_preview')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': (
                'name', 'author', 'text', 'cooking_time',
                'image', 'image_preview'
            )
        }),
        ('Дополнительно', {
            'fields': ('favorites_count',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(fav_count=Count('favorites'))

    def favorites_count(self, obj):
        return obj.fav_count
    favorites_count.short_description = 'В избранном'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" '
                'style="max-height: 100px; max-width: 100px;" />',
                obj.image.url
            )
        return 'Нет изображения'
    image_preview.short_description = 'Превью'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__name')
    autocomplete_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__name')
    autocomplete_fields = ('user', 'recipe')
