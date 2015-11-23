from django.db import models
from django.core.urlresolvers import reverse

import uuid
import os

def get_article_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('article/images', filename)

class ArticleCategory(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.CharField(max_length=200,null=True)
        
    def __unicode__(self):
        return self.name
    
def get_default_category():
    return ArticleCategory.objects.get_or_create(name="Uncategorized", slug='uncategorized')[0]

class Author(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.CharField(max_length=200,null=True)

    def __unicode__(self):
        return self.name

class ArticleImage(models.Model):
    cover_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_article_image_path,null=True,blank=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    published_on = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey("ArticleCategory", default=get_default_category, on_delete=models.SET_DEFAULT)
    author= models.ForeignKey("Author",null=True,on_delete=models.SET_NULL)
    summary = models.CharField(max_length=400)
    content = models.TextField()
    images = models.ManyToManyField("ArticleImage",null=True,blank=True)
    is_featured = models.BooleanField(default=False,blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_cover_image(self):
        try:
            cover_image = self.images.filter(cover_image = True)[0]
            if cover_image:
                return cover_image
            else:
                return False
        except:return False

    def get_images(self):
        try:
            images = self.images.filter(cover_image = False)
            if images.exists():
                return images
            else:
                return False
        except:return False

    def get_absolute_url(self):
        url = '/articles/' +self.slug+'.html'
        return url

