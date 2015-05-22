from django.http.response import HttpResponseNotFound
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect

from rest_framework import generics

from .models import Folder, Ad
from . import serializers
from .import const as msg
from core.views import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class FolderListView(ListCreateAPIView):
    """Folder API for operations read (multiple) and create."""

    queryset = Folder.objects.active()
    serializer_class = serializers.FolderSerializer


class FolderDetailView(RetrieveUpdateDestroyAPIView):
    """Folder API for operations read, update and delete."""

    queryset = Folder.objects.active()
    serializer_class = serializers.FolderSerializer

    def perform_destroy(self, instance):
        """Deactivates current folder and all it's children folders."""

        with transaction.atomic():
            super().perform_destroy(instance)
            self.delete_children(instance)

    def delete_children(self, instance):
        """Recursively deletes child folders and their corresponding ads."""

        for child in instance.children.active():
            self.delete_children(child)

        instance.children.active().update(is_active=False)
        instance.ads.active().update(is_active=False)


class AdListView(generics.ListCreateAPIView):
    """Ad API for operations read (multiple) and create."""

    queryset = Ad.objects.active()
    serializer_class = serializers.AdSerializer


class AdDetailView(RetrieveUpdateDestroyAPIView):
    """Ad API for operations read, update and delete."""

    queryset = Ad.objects.active()
    serializer_class = serializers.AdSerializer


class FolderAdView(generics.RetrieveAPIView):
    """
    API which returns structure of current folder. Structure contains all immediate sub-folders
    (only for one level) and ads for current folder.
    """

    queryset = Folder.objects.active()
    serializer_class = serializers.FolderAdSerializer


def folder_ad_default(request):
    """Redirects url with no path to root folder view."""

    try:
        root_folder = Folder.objects.active().get(parent=None)
    except Folder.DoesNotExist:
        return HttpResponseNotFound(msg.MSG_ROOT_FOLDER_DOESNT_EXIST)

    return redirect(reverse('folder-ad-detail', args=(root_folder.pk,)))


class AdCreatorTemplateView(TemplateView):
    """View which servers html page for ad creator."""

    template_name = 'ads/ad_creator.html'
