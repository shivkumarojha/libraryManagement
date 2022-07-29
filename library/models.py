from django.db import models
from registration.models import ClassName, Section
from libraryManagement import settings

class Book(models.Model):
    bookName = models.CharField(max_length=100, null=False, blank=False)
    authorName = models.CharField(max_length=100, null=False, blank=False)
    isbn = models.CharField(max_length=100, null=False, blank=False, unique=True)
    className = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)    
    updated_date = models.DateTimeField(auto_now=True)
    quantity = models.SmallIntegerField()
    stock = models.SmallIntegerField(null=True, blank=True)    
    def __str__(self):
        return f'{self.className} {self.bookName} by {self.authorName} '

class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey((settings.AUTH_USER_MODEL), on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    expected_date_of_return = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    returned = models.BooleanField(default=False)
    date_of_return = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    fine = models.SmallIntegerField(null=True,blank=True)
    
    def __str__(self):
        return f'{self.book.className} {self.book.bookName} '
        # return self.book.bookName
    @property
    def is_returned(self):
        return self.returned
    # @property
    # def issued_date(self):
    #     return self.issued_date