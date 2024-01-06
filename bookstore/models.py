from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
import uuid
from django.utils import timezone
# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
class Genre(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.name
class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    genre=models.ForeignKey(Genre,on_delete=models.CASCADE)
    price=models.IntegerField()
    description=models.TextField()
    book_image=models.ImageField()
    def __str__(self) -> str:
        return self.title
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self)->str:
        return f"User {self.user.username} order"
class CartHistory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self)->str:
        return f"User {self.user.username} ordered History"
class EmailTokenGeneration(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    token=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    created_at=models.DateField(default=timezone.now)
    def __str__(self) -> str:
        return str(self.token)
class Comment(models.Model):
    value=models.TextField(blank=False)
    comment_user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.comment_user.username} comment on {self.book.title}"
class Wishlist(models.Model):
    wish_user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    def __str__(self):
        return f"Wishlist for {self.wish_user.username}"