from django.db import models
from django.urls import reverse

# Create your models here.


# post tags
class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    posts = models.ManyToManyField('Post', through="PostTags")

# post
class Post(models.Model):
    headline=models.CharField(max_length=255)
    slug=models.CharField(max_length=130, unique=True)
    #slug = models.SlugField(null=False, unique=True, max_length = 250)
    content=models.TextField()
    created_on=models.DateTimeField('date created', auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    view_count=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    #image = models.ImageField(upload_to="images", blank=True, null=True)
    #image = models.FileField(upload_to='images/', null=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    tags = models.ManyToManyField('Tag', through="PostTags")
   
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.headline


    

# post tags join table
class PostTags(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


# post comment
class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(default='anonymous', max_length = 100)
    authorEmail = models.EmailField(null=True, max_length = 250)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.content[:60]