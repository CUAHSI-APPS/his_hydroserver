from django.db import models


class Collection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    collection_id = models.TextField(unique=True)

    class Meta:
        ordering = ('created',)


class Database(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    collection_id = models.TextField()
    database_id = models.TextField()
    database_name = models.TextField(default="None")
    database_path = models.TextField(default="None")
    database_type = models.TextField(default="None")

    class Meta:
        ordering = ('created',)
        unique_together = ('collection_id', 'database_id',)
