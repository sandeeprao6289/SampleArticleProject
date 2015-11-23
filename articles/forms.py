from django import forms
from django.utils.translation import ugettext as _
from articles.models import Article, ArticleCategory, Author

valid_date_formats = ['%m/%d/%Y']

class ArticleForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':_('Enter Article Title'),'autocomplete':'off','onkeyUp':'string_to_slug(this.value)'}),error_messages={'required': _('Please enter the  title')})
    category = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'form-control','placeholder':_('Choose a category')}),queryset=ArticleCategory.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select a category')})
    author = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'form-control','placeholder':_('Choose an author')}),queryset=Author.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select an author')})
    summary = forms.CharField(required=True, max_length=400,widget=forms.Textarea(attrs={'maxlength':400,'style':'max-width:566px;', 'rows': '4','class': 'form-control', 'placeholder': "Enter a short summary concerning about this article in this text box"}),error_messages={'required': _('Please enter the summary')})
    content = forms.CharField(required=True,widget=forms.Textarea(attrs={'rows':'8','class':'form-control'}),error_messages={'required': _('Please enter the content')})
    
    class Meta:
        model = Article
        fields = ('title','summary','content','category','author')