from django.db import models


class Network(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    network_id = models.TextField(unique=True)

    class Meta:
        ordering = ("created",)


class Database(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    network_id = models.TextField()
    database_id = models.TextField()
    database_name = models.TextField(default="None")
    database_path = models.TextField(default="None")
    database_type = models.TextField(default="None")

    class Meta:
        ordering = ("created",)
        unique_together = ("network_id", "database_id",)


class Reference(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	site_name = models.TextField(default=None, blank=True, null=True)
	site_code = models.TextField()
	latitude = models.FloatField()
	longitude = models.FloatField()
	variable_name = models.TextField(default=None, blank=True, null=True)
	variable_code = models.TextField()
	sample_medium = models.TextField(default=None, blank=True, null=True)
	value_count = models.IntegerField(default=None, blank=True, null=True)
	begin_date = models.DateTimeField(default=None, blank=True, null=True)
	end_date = models.DateTimeField(default=None, blank=True, null=True)
	method_link = models.TextField(default=None, blank=True, null=True)
	method_description = models.TextField(default=None, blank=True, null=True)
	network_id = models.TextField()
	database_id = models.TextField()

	class Meta:
		ordering = ("created",)
		unique_together = ("network_id", "database_id", "site_code", "variable_code",)
