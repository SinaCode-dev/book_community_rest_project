from django.contrib import admin

from .models import Book, Category, BookCase, BookCaseItem, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = ['user', 'body', 'status', 'datetime_created']
    extra = 1
    readonly_fields = ['datetime_created']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'score', 'author']
    inlines = [CommentsInline]


class BookInline(admin.TabularInline):
    model = Book
    fields = ['name', 'cover', 'description', 'category', 'score', 'author', 'publications', 'num_of_pages', 'date_writed']
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'top_book']
    inlines = [BookInline]


class BookCaseItemInline(admin.TabularInline):
    model = BookCaseItem
    fields = ['id', 'book', 'status']
    extra = 1


@admin.register(BookCase)
class BookCaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    inlines = [BookCaseItemInline]

    def has_delete_permission(self, request, obj = None):
        return False


@admin.register(BookCaseItem)
class BookCaseItemAdmin(admin.ModelAdmin):
    list_display = ['bookcase', 'book', 'status', 'datetime_added']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'body', 'datetime_created']