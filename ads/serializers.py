from rest_framework import serializers

from .models import Folder, Ad


class FolderSerializer(serializers.ModelSerializer):
    """Folder serializer for CRUD operations."""

    class Meta:
        model = Folder
        fields = ('pk', 'url', 'name', 'parent')
        # Limits parent folders to active folders.
        extra_kwargs = {
            'parent': {'queryset': Folder.objects.active()}
        }


class AdSerializer(serializers.ModelSerializer):
    """Ad serializer for CRUD operations."""

    class Meta:
        model = Ad
        fields = ('pk', 'url', 'name', 'ad_url', 'folder')
        # Limits folders to active folders.
        extra_kwargs = {
            'folder': {'queryset': Folder.objects.active()}
        }


class FolderRelatedSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for related folder field."""

    class Meta:
        model = Folder
        fields = ('pk', 'url', 'name')
        extra_kwargs = {'url': {'view_name': 'folder-ad-detail'}}


class AdRelatedSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for related ad field."""

    class Meta:
        model = Ad
        fields = ('ad_url', 'name')


class FolderAdSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for folder structure. Contains folder children and ads."""

    parent = FolderRelatedSerializer()
    children = serializers.SerializerMethodField('filter_active_folders')
    ads = serializers.SerializerMethodField('filter_active_ads')

    class Meta:
        model = Folder
        fields = ('pk', 'name', 'parent', 'children', 'ads')
        extra_kwargs = {'url': {'view_name': 'folder-ad-detail'}}

    def _get_serialized_data(self, serializer_class, instance):
        """Helper function for data serialization."""

        serializer = serializer_class(
            instance, context={'request': self.context['request']}, many=True
        )

        return serializer.data

    def filter_active_folders(self, obj):
        """Filter for active folders. Needed for related field 'children'."""

        return self._get_serialized_data(FolderRelatedSerializer, obj.children.active())

    def filter_active_ads(self, obj):
        """Filter for active ads. Needed for related field 'ads'."""

        return self._get_serialized_data(AdRelatedSerializer, obj.ads.active())
