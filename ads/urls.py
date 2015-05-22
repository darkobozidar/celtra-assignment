from django.conf.urls import url

from . import views


urlpatterns = [
    # CRUD API for folders
    url(r'^folders/$', views.FolderListView.as_view(), name='folder-list'),
    url(r'^folders/(?P<pk>\d+)/$', views.FolderDetailView.as_view(), name='folder-detail'),
    # CRUD API for ads
    url(r'^ads/$', views.AdListView.as_view(), name='ad-list'),
    url(r'^ads/(?P<pk>\d+)/$', views.AdDetailView.as_view(), name='ad-detail'),
    # API for list of folders and ads
    url(r'^folder_ad/$', views.folder_ad_default, name='folder-ad-detail'),
    url(r'^folder_ad/(?P<pk>\d+)/$', views.FolderAdView.as_view(), name='folder-ad-detail'),
]


urlpatterns += [
    url(r'^$', views.AdCreatorTemplateView.as_view(), name='ad-creator'),
]
