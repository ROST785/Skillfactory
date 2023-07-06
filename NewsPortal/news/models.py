from django.db import models


class Author(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        return self.rating


class Category(models.Model):
    category_name = models.CharField(unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(choices=['Статья', 'Новость'])
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField('PostCategory')
    header = models.CharField()
    text = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        return self.rating

    def dislike(self):
        self.rating -= 1
        return self.rating

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()
    comment_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        return self.rating

    def dislike(self):
        self.rating -= 1
        return self.rating