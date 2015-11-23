# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from articles.models import Article, ArticleCategory, Author, ArticleImage
from articles.forms import ArticleForm

def list_articles(request, template="article/article-home.html"):
    data = {}

    featured_article = Article.objects.filter(is_featured = True).order_by('?')[:1]
    featured_articles = Article.objects.filter(is_featured = True).exclude(id__in = [featured_article[0].id]).order_by('-id')[:4]
    articles = Article.objects.filter(is_featured = False)
    
    data['featured_article'] = featured_article
    data['featured_articles'] = featured_articles
    data['articles'] = articles
    
    return TemplateResponse(request, template, data)

def article_details(request,slug,template="article/article-details.html"):
    
    article = Article.objects.get(slug = slug)
    data = {}
    data['article'] = article
    articles = Article.objects.all().exclude(id__in = [article.id]).order_by('?')[:4]
    data['articles'] =articles
    return TemplateResponse(request, template, data)

def add_article(request, template="article/add-article.html"):
    data = {}
    try:
        aid = request.REQUEST.get('aid')
        article = Article.objects.get(id = aid)
        data['article'] = article
        form = ArticleForm(instance = article)
    except:
        article = False
        form = ArticleForm()
    if request.POST:
        if article:form = ArticleForm(request.POST,instance = article)
        else:form = ArticleForm(request.POST)
        
        if form.is_valid():
            savearticleform = form.save(commit=False)
            savearticleform.slug = slugify(savearticleform.title)
            savearticleform.save()
            cover_image_id = request.POST.get('cover_image',False)
            if cover_image_id:
                cover_image = ArticleImage.objects.get(id = int(cover_image_id))
                savearticleform.images.add(cover_image)
                
            photo_ids = request.POST.getlist('images',[])
            is_featured = request.POST.get('is_featured')
            if is_featured == 'True':
                savearticleform.is_featured = True
            else:
                savearticleform.is_featured = False
            if photo_ids:
                for photoid in photo_ids:
                    image = ArticleImage.objects.get(id = int(photoid))
                    savearticleform.images.add(image)
            savearticleform.save()
            return HttpResponseRedirect(reverse('list_articles'))
            
    data['form'] = form
    return TemplateResponse(request, template, data)


def delete_article(request):
    aid = request.REQUEST.get('aid')
    article = Article.objects.get(id = aid)
    article.delete()
    return HttpResponseRedirect(reverse('list_articles'))
    


def delete_image(request):
    data={}
    id = request.REQUEST.get('id')
    image = ArticleImage.objects.get(id = id)
    image.delete()
    
    data['status'] = 1
    return HttpResponse(simplejson.dumps(data))

@csrf_exempt
def upload_article_image(request):
    data = {}
    sdata = {}
    file = request.FILES['articleimage']
    iscover = request.REQUEST.get('cover',False)
    try:
        image = ArticleImage()
        image.image = file
        if iscover:image.cover_image = True
        image.save()
        sdata['image'] = image
        if iscover:sdata['cover_image'] = True
        data['html']=render_to_string('article/include-article-image.html',sdata,context_instance=RequestContext(request))
        if iscover:data['cover'] = 1
    except:
        pass
    data['status'] = 1
    return HttpResponse(simplejson.dumps(data))

######################################################ARTICLE CATEGORIES VIEWS START################################################
def categories(request, template="article/categories.html"):
    data = {}
    categories = ArticleCategory.objects.all()
    data['categories'] = categories
    return TemplateResponse(request, template, data)

@csrf_exempt
def add_category(request):
    data = {}
    sdata = {}
    id = request.REQUEST.get('catid',False)
    if id:
        category = ArticleCategory.objects.get(id = int(id))
        if not request.POST:data['category'] = category
        
    if request.method=='POST':
        if not id:
            category = ArticleCategory()
        category.name = name = request.POST.get('name')
        category.slug = slugify(name)
        category.save()
        categories = ArticleCategory.objects.all()
        sdata['categories'] = categories
        data['html']=render_to_string('article/include-article-categories.html',sdata,context_instance=RequestContext(request))
        data['status'] = 1
        return HttpResponse(simplejson.dumps(data))
    #else:return HttpResponse('0')
    return render_to_response('article/add-category.html',data,context_instance=RequestContext(request))

def delete_category(request):
    data = {}
    sdata = {}
    id = request.GET.get('id',False)
    
    category = ArticleCategory.objects.get(id = int(id))
    category.delete()
    data['status'] = 1
    return HttpResponse(simplejson.dumps(data))

######################################################ARTICLE CATEGORIES VIEWS END################################################
######################################################ARTICLE AUTHOR VIEWS START################################################

def authors(request, template="article/authors.html"):
    data = {}
    authors = Author.objects.all()
    data['authors'] = authors
    return TemplateResponse(request, template, data)

@csrf_exempt
def add_author(request):
    data = {}
    sdata = {}
    id = request.REQUEST.get('authid',False)
    if id:
        author = Author.objects.get(id = int(id))
        if not request.POST:data['author'] = author
        
    if request.method=='POST':
        if not id:
            author = Author()
        author.name = name = request.POST.get('name')
        author.slug = slugify(name)
        author.save()
        authors = Author.objects.all()
        sdata['authors'] = authors
        data['html']=render_to_string('article/include-article-authors.html',sdata,context_instance=RequestContext(request))
        data['status'] = 1
        return HttpResponse(simplejson.dumps(data))
    #else:return HttpResponse('0')
    return render_to_response('article/add-author.html',data,context_instance=RequestContext(request))


def delete_author(request):
    data = {}
    sdata = {}
    id = request.GET.get('id',False)
    
    author = Author.objects.get(id = int(id))
    author.delete()
    data['status'] = 1
    return HttpResponse(simplejson.dumps(data))

######################################################ARTICLE AUTHOR VIEWS END################################################    
        
        
