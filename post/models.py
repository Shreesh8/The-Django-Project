from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
#from django.utils.text import slugify

AUTH_USER_MODEL = 'post.User'

class Post(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="Yazar", related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=200,verbose_name="Title ")
    desc = RichTextField(verbose_name="")
    date = models.DateTimeField(verbose_name="Date/Time ", auto_now_add=True)
    image = models.ImageField(upload_to='images_uploaded', null=True, blank=True)
    video = models.FileField(upload_to='videos_uploaded',null=True, blank=True,
    validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    upvotes = models.PositiveIntegerField(default=0)
    post_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_update_url(self):
        return reverse('post:update', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_create_url(self):
        return reverse('post:create')
        #return "/user/{}".format(self.id)

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_delete_post_adminpanel_url(self):
        return reverse('post:delete_post_adminpanel', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_delete_url_home(self):
        return reverse('home:delete_home', kwargs={'id': self.id})       # worst naming i have ever seen ... FIX IT
        #return "/user/{}".format(self.id)

    #def set_user_perms_staff_adminpanel(self):
    #    print("working2")
    #    return reverse('post:change_user_staff_perms', kwargs={'id': self.id})
    #    #return "/user/{}".format(self.id)

    #def set_user_perms_superusr_adminpanel(self):
    #    return reverse('post:change_user_superusr_perms', kwargs={'id': self.id})
    #    #return "/user/{}".format(self.id)
    
    #def get_unique_slug(self):
    #    slug = slugify(self.title.replace('ı', 'i'))
    #    unique_slug = slug
    #    counter = 1
    #    while Post.objects.filter(slug=unique_slug).exists():
    #        unique_slug = '{}-{}'.format(slug, counter)
    #        counter += 1
    #    return unique_slug

    #def save(self, *args, **kwargs):
    #    return super(Post, self).save(*args, **kwargs)
    #    self.slug = self.get_unique_slug()

    class Meta:
        ordering = ["-date","id"]


class UserUpvote(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="upvotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_upvotes")

    class Meta:
        unique_together = ("user","post")

class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User' ,null=True,blank=True,verbose_name="Yazar", on_delete=models.SET_NULL)
    name = models.CharField(max_length=200,verbose_name="Name ")
    content = RichTextField(verbose_name="")
    created_date = models.DateTimeField(verbose_name="Created Date ", auto_now_add=True)
    

class ContactInfo(models.Model):
    user = models.ForeignKey('auth.User' ,null=True,blank=True,verbose_name="Yazar", on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200,verbose_name="Name")
    surname = models.CharField(max_length=200,verbose_name="Surname")
    
    select_gender = (
        ('Other', 'Other'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user_gender = models.CharField(max_length=8, choices=select_gender, default="other")

    adress = models.CharField(max_length=200,verbose_name="Adress")
    email = models.EmailField(verbose_name="Email")        
    
    def get_delete_contact_adminpanel_url(self):
        return reverse('post:delete_contact_adminpanel', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)

    def get_modify_contact_adminpanel_url(self):
        return reverse('post:modify_contact_adminpanel', kwargs={'id': self.id})
        #return "/user/{}".format(self.id)