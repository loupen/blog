from django.db import models

# Create your models here.
class Author(models.Model):
	author = models.CharField(max_length=10)
	pic = models.ImageField(upload_to="static/page/img")
	email = models.EmailField(null=True)
	wchat = models.CharField(max_length=20,null=True);
	brief = models.TextField();
	def __str__(self):
		return self.author

class Tag(models.Model):
	tag = models.CharField(max_length=20)
	def __str__(self):
		return self.tag

class Content(models.Model):
	txt_title = models.CharField(max_length=80)
	txt_body = models.TextField()
	txt_date = models.DateTimeField('published')
	txt_author = models.ForeignKey(Author, on_delete=models.CASCADE)
	txt_tag = models.ManyToManyField(Tag)
	def __str__(self):
		return self.txt_title

