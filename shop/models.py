from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	