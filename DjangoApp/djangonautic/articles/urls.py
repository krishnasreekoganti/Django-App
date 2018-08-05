from django.conf.urls import url
from . import views

app_name = 'articles'

urlpatterns = [
    url(r'^$', views.article_list, name="list"),
    url(r'^create/$', views.article_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/$', views.article_detail, name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/',views.article_update,name = "update" ),
    url(r'^(?P<slug>[\w-]+)/delete/',views.article_delete,name = "delete" ),
    url(r'^(?P<slug>[\w-]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]
