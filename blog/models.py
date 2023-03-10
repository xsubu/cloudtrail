from django.db import models
from django.urls import reverse

# Create your models here.


# post tags
class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

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
    tags = models.ManyToManyField(to=Tag, related_name="posts", blank=True)
   
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.headline



# post comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(default='anonymous', max_length = 100)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
