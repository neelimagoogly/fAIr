from django.contrib.gis.db import models as geomodels
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from login.models import OsmUser

# Create your models here.


class Dataset(models.Model):
    class DatasetStatus(models.IntegerChoices):
        ARCHIVED = 1
        ACTIVE = 0
        DRAFT = -1

    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(OsmUser, to_field="osm_id", on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source_imagery = models.URLField(blank=True, null=True)
    status = models.IntegerField(
        default=-1, choices=DatasetStatus.choices
    )  # 0 for active , 1 for archieved


class AOI(models.Model):
    class DownloadStatus(models.IntegerChoices):
        DOWNLOADED = 1
        NOT_DOWNLOADED = -1
        RUNNING = 0

    dataset = models.ForeignKey(Dataset, to_field="id", on_delete=models.CASCADE)
    geom = geomodels.PolygonField(srid=4326)
    download_status = models.IntegerField(default=-1, choices=DownloadStatus.choices)
    last_fetched_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Label(models.Model):
    aoi = models.ForeignKey(AOI, to_field="id", on_delete=models.CASCADE)
    geom = geomodels.GeometryField(srid=4326)
    osm_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Model(models.Model):
    class ModelStatus(models.IntegerChoices):
        ARCHIVED = 1
        PUBLISHED = 0
        DRAFT = -1

    dataset = models.ForeignKey(Dataset, to_field="id", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(OsmUser, to_field="osm_id", on_delete=models.CASCADE)
    published_training = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(default=-1, choices=ModelStatus.choices)  #


class Training(models.Model):
    STATUS_CHOICES = (
        ("SUBMITTED", "SUBMITTED"),
        ("RUNNING", "RUNNING"),
        ("FINISHED", "FINISHED"),
        ("FAILED", "FAILED"),
    )
    model = models.ForeignKey(Model, to_field="id", on_delete=models.CASCADE)
    source_imagery = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=STATUS_CHOICES, default="SUBMITTED", max_length=10
    )
    task_id = models.CharField(null=True, blank=True, max_length=100)
    zoom_level = ArrayField(
        models.PositiveIntegerField(),
        size=4,
    )
    created_by = models.ForeignKey(OsmUser, to_field="osm_id", on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    epochs = models.PositiveIntegerField()
    batch_size = models.PositiveIntegerField()
    freeze_layers = models.BooleanField(default=False)


class Feedback(models.Model):
    ACTION_TYPE = (
        ("CREATE", "CREATE"),
        ("MODIFY", "MODIFY"),
        ("ACCEPT", "ACCEPT"),
        ("INITIAL", "INITIAL"),
    )
    geom = geomodels.GeometryField(srid=4326)
    training = models.ForeignKey(Training, to_field="id", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    zoom_level = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(23)]
    )
    action = models.CharField(choices=ACTION_TYPE, max_length=10)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(OsmUser, to_field="osm_id", on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
