from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('articles.views',
    url(r'^/?$', 'list_articles', name="list_articles"),
    url(r'^add-article/?$', 'add_article', name="add_article"),
    url(r'^delete-article/?$', 'delete_article', name="delete_article"),
    url(r'^delete-image/?$', 'delete_image', name="delete_image"),
    
    url(r'^categories/?$', 'categories', name="categories"),
    url(r'^add-category/?$', 'add_category', name="add_category"),
    url(r'^delete-category/?$', 'delete_category', name="delete_category"),
    
    url(r'^authors/?$', 'authors', name="authors"),
    url(r'^add-author/?$', 'add_author', name="add_author"),
    url(r'^delete-author/?$', 'delete_author', name="delete_author"),
    
    url(r'^upload-article-image/', 'upload_article_image', name='upload_article_image'),
    
    url(r'^(?P<slug>[-\w]+)(.html)\/?$', 'article_details'),
    
)
