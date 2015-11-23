
from django.template import Template
from django.template.response import TemplateResponse

def home(request, template="frontend/home.html"):
    ''' index page methods '''
    data = {}
    
    return TemplateResponse(request, template, data)
