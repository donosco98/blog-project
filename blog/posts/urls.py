from django.conf.urls import url,include

from . import views
urlpatterns = [

    url(r'^create/$',views.post_create),
    url(r'^(?P<slug>[\w-]+)/$',views.post_detail,name="detail"),
    url(r'^$',views.post_list,name="lists"),
    url(r'^(?P<slug>[\w-]+)/edit/$',views.post_update),
    url(r'^(?P<slug>[\w-]+)/delete/$',views.post_delete),


]
