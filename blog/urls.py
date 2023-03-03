from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [

    #using predefined class from django
    path('', TemplateView.as_view(template_name = 'blog/default.html')),
    path('show', views.showAll, name='show'),
    path('showdetail/<str:slug>/', views.showDetail, name='detail'),
    path('add', views.AddPost, name='addpost'),
    path('editpost/<str:slug>/', views.editPost, name='editpost'),
    path('deletepost/<str:slug>/', views.deletePost, name='deletepost'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)