from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'gyoseki'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recode_id>', views.detail, name='detail'),
    path('<int:recode_id>/update', views.update, name='update'),
    path('<int:recode_id>/bibtex', views.bibtex, name='bibtex'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author_detail, name='author_detail'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:tag_id>', views.tag_detail, name='tag_detail'),
    path('tags/register', views.tag_register, name='tag_register'),
    path('search/', views.search, name='search'),
    path('search/download', views.download, name='download'),
    path('register/', views.register, name='register'),
    path('man/', views.man, name='man'),
]