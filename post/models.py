from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

#from django.utils.text import slugify

class Post(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="Yazar", related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=200,verbose_name="Title ")
    desc = RichTextField(verbose_name="Description ")
    date = models.DateTimeField(verbose_name="Date/Time ", auto_now_add=True)
    image = models.ImageField(null=True, blank=True)

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


class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)

    name = models.CharField(max_length=200,verbose_name="Name ")
    content = RichTextField(verbose_name="Comment ")
    created_date = models.DateTimeField(verbose_name="Created Date ", auto_now_add=True)
    