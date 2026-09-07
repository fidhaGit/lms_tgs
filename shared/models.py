from django.db import models
from django.utils import timezone
from datetime import datetime

class AutoDateTimeField(models.DateTimeField):
	def pre_save(self, model_instance, add):
		return timezone.now()

class BaseModel(models.Model):
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = AutoDateTimeField(default=timezone.now)
	class Meta:
		abstract = True

	def strftime_created_at(self):
		return self.created_at.strftime("%d/%m/%Y, %H:%M:%S")

	def strftime_updated_at(self):
		return self.created_at.strftime("%d/%m/%Y, %H:%M:%S")
	
	@classmethod
	def to_date_time(self,timestamp):
		return datetime.fromtimestamp(timestamp)

	@classmethod
	def to_timestamp(self, time):
		return datetime.timestamp(time)