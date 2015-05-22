from django.core.exceptions import ValidationError
from django.db import models

from . import const
from core.models import IsActiveModel, BaseTimeModel


class Folder(IsActiveModel, BaseTimeModel):
    """Represents folder. Folder can contain multiple sub-folders and ads."""

    name = models.CharField(max_length=100, help_text='Name of the folder.')
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        help_text='Reference to parent folder.'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def clean(self):
        """Additional model validations."""

        # Validates if folder is parent to itself.
        if self.parent == self:
            raise ValidationError({'parent': const.MSG_FOLDER_CANT_BE_PARENT_TO_ITSELF})

        # Validations for root folder
        if self.is_root:
            root_folders = Folder.objects.active().filter(parent=None)
            # In case of update current folder has to be excluded
            if self.pk:
                root_folders = root_folders.exclude(pk=self.pk)
            root_folders_exist = root_folders.exists()

            if self.is_active and root_folders_exist:
                raise ValidationError(const.MSG_ONLY_ONE_ROOT_FOLDER)
            elif not self.is_active and not root_folders_exist and Folder.objects.active().exists():
                raise ValidationError(const.MSG_ROOT_FOLDER_CANT_DELETE)

        super().clean()

    @property
    def is_root(self):
        """Designates whether this folder is root folder."""

        return self.parent is None

    @property
    def is_active_root(self):
        """Designates whether this folder is active root folder."""

        return self.is_root and self.is_active


class Ad(IsActiveModel, BaseTimeModel):
    """Represents ad. One ad belongs to one folder."""

    name = models.CharField(max_length=100, help_text="Name of the ad.")
    ad_url = models.URLField(help_text='Url to the ad.')
    folder = models.ForeignKey(
        Folder, related_name='ads', help_text='Folder to which ad belongs to.'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def clean(self):
        """Additional model validations."""

        if self.folder and not self.folder.is_active:
            raise ValidationError({'folder': const.MSG_AD_HAS_TO_BELONG_TO_FOLDER})
        super().clean()
