from django.db import models


class BasePackage(models.Model):
    """
    Base Package model which can be subclassed to add additional fields.

    PROCESS_STATUS_CHOICES is expected to be overridden by child models.
    """
    bag_identifier = models.CharField(max_length=255, unique=True)
    bag_path = models.CharField(max_length=255, null=True, blank=True)
    TYPE_CHOICES = (
        ('aip', 'Archival Information Package'),
        ('dip', 'Dissemination Information Package'),
    )
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        null=True,
        blank=True)
    ORIGIN_CHOICES = (
        ('aurora', 'Aurora'),
        ('legacy_digital', 'Legacy Digital Processing'),
        ('digitization', 'Digitization')
    )
    origin = models.CharField(
        max_length=20,
        choices=ORIGIN_CHOICES,
        default='aurora')
    PROCESS_STATUS_CHOICES = (None)
    process_status = models.IntegerField(choices=PROCESS_STATUS_CHOICES)
    data = models.JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
