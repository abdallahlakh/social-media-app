from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.
class Publication(models.Model):
    likes_num=models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=10)
    description=models.TextField()
    img=models.ImageField(upload_to='pics')
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    
class Like(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    publication=models.ForeignKey(Publication, on_delete=models.CASCADE,null=True,blank=True)
    status=models.BooleanField(default=False)

class Profile(models.Model):
    followers_num=models.IntegerField(default=0)
    following_num=models.IntegerField(default=0)
    post_num=models.IntegerField(default=0)
    profile_img=models.ImageField(upload_to='pics')
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    username=models.CharField(max_length=10)
    
class Follow(models.Model):
    user_follower_id=models.IntegerField()
    user_followed_id=models.IntegerField()
    following_status=models.BooleanField(default=False)

    
class Comment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    publication=models.ForeignKey(Publication, on_delete=models.CASCADE,null=True,blank=True)
    content=models.CharField(max_length=30)
    created=models.DateTimeField(auto_now_add=True)