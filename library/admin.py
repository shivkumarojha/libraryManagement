from django.contrib import admin
from .models import Book, Issue

class BookAdmin(admin.ModelAdmin):
    list_display = ('className','bookName', 'authorName', 'quantity', 'stock')
admin.site.register(Book, BookAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'issued_date', 'expect_date_of_return','fine')
admin.site.register(Issue, IssueAdmin)