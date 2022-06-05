import uuid
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save,post_delete
from django.urls import reverse

# Create your models here.

# Profile
# Image/Post
# Comment

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pic_name = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='feed_images',blank=True)
    caption = HTMLField() 
    post_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post-details',args=[str(self.id)])

    def __str__(self):
        return f"{self.caption}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')

    def __str__(self):
        return f"{self.follower}"


# view followers posts
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='stream_following')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post =instance
        user = post.user
        followers = Follow.objects.all().filter(following=user) 

        for follower in followers:
            stream =Stream(post=post,user=follower.follower,date=post.post_date,following=user)
            stream.save()
        # signal
        post_save.connect(Stream.add_post, sender=Post)
