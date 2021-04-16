from django.db import models

# Create your models here.

class userinfo(models.Model):
	#strores the user info
	username = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)
	email = models.CharField(max_length = 200)
	category = models.CharField(max_length = 200)

	def __str__(self):
		return self.username

	def getRankings(self):
		l = [int(i) for i in self.category.split(",")]
		return l

class book(models.Model):
	name = models.CharField(max_length = 200)
	author = models.CharField(max_length = 200)
	rating = models.FloatField()
	category = models.CharField(max_length = 200)
	image = models.CharField(max_length = 1000)

	def __str__(self):
		return self.name

