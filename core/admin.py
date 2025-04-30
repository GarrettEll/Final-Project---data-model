from django.contrib import admin
from .models import Post, Comment, Category, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'timestamp', 'parent')
    list_filter = ('timestamp',)
    search_fields = ('author__username', 'content')
    ordering = ('-timestamp',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_author')
    list_filter = ('is_author',)


# Customize the admin site header and title
admin.site.site_header = "CampusConnect Administration"
admin.site.site_title = "CampusConnect Admin Portal"
admin.site.index_title = "Welcome to CampusConnect Admin"