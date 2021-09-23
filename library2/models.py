
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Genre(models.Model):
    sno = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class Books(models.Model):
    sno = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 60,blank = False)
    author = models.CharField(max_length = 100)
    genre = models.ManyToManyField(Genre,blank = True)
    borrowed = models.BooleanField(default = False)
    desc= models.TextField(default= '')
                                  
    image = models.ImageField(blank = False,upload_to = 'books/')
    


    def __str__(self):
         return self.name

class UserInfo(models.Model):
    username = models.OneToOneField(User,on_delete = models.CASCADE)
    books_borrowed= models.ManyToManyField(Books,blank = True)
    preferences = models.ManyToManyField(Genre,blank = True)

    def __str__(self):
        return self.username.username


class Comment(models.Model):
    id = models.AutoField(primary_key = True)
    commenter = models.ForeignKey(User,on_delete  = models.CASCADE)
    content = models.TextField(default = '')
    book_name=  models.ForeignKey(Books,on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.commenter.first_name} on {self.book_name.name}'