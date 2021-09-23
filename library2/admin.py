from django.contrib import admin
from .models import Books,Genre,UserInfo,Comment
# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    list_display = ('name', 'author','borrowed')
    filter_horizontal= ('genre',)
class GenreAdmin(admin.ModelAdmin):
    filter_horizontal = ('preferences','books_borrowed')

admin.site.register(Genre)
#admin.site.register(BorrowedBooks)

admin.site.register(Books,BooksAdmin)  
admin.site.register(UserInfo,GenreAdmin)  
admin.site.register(Comment)  



admin.site.site_header = "Ningombam Library"