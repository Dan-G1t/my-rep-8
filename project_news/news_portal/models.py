from django.db import models
from django.contrib.auth.models import User
from news_portal.resources import CONTENT_TYPES, article
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.FloatField(default = 0)

    def update_rating(self):
        author_posts = Post.objects.filter(author = self)
        sum_posts_rating = sum(post.rating for post in author_posts) * 3
        author_comments = Comment.objects.filter(user = self.user)
        sum_author_comments_rating = sum(comment.rating for comment in author_comments)
        sum_posts_comments_rating = sum(comment.rating for post in author_posts for comment in Comment.objects.filter(post=post))
        self.rating = sum_posts_rating + sum_author_comments_rating + sum_posts_comments_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    content_type = models.CharField(max_length = 1, choices = CONTENT_TYPES, default = article)
    creation_date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255)
    text = models.TextField()
    rating = models.FloatField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return f"{self.text[:124]}..."
        else:
            return self.text
        
    def __str__(self):
        return f'{self.title}: {self.text[:120]}'
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    rating = models.FloatField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
