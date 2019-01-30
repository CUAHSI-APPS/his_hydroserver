from django.db import models


class Network(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    network_id = models.TextField(unique=True)

    class Meta:
        ordering = ('created',)


class Database(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    network_id = models.TextField()
    database_id = models.TextField()
    database_name = models.TextField(default="None")
    database_path = models.TextField(default="None")
    database_type = models.TextField(default="None")

    class Meta:
        ordering = ('created',)
        unique_together = ('network_id', 'database_id',)
