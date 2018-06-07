from django.contrib import admin

# Register your models here.
from .models import Author,Content,Tag
from .forms import *
import re

class ContentAdmin(admin.ModelAdmin):
	file_lable= ''
	file_name = ''
	fieldsets = [
		('Title', {'fields':['txt_title']}),
		('Author', {'fields':['txt_author']}),
		('Date', {'fields':['txt_date']}),
		('Tag', {'fields':['txt_tag']}),
		('Body Content', {'fields':['txt_body']}),	
	]
	list_dispaly = ('txt_title', 'txt_author', 'txt_date', 'txt_tag', 'txt_body')
	def delete_view(self, request, object_id, extra_context=None):
		delete_file(object_id)
		return super().delete_view(
			request, object_id, extra_context=extra_context,
		)
	def change_view(self, request, object_id, form_url='', extra_context=None):
		extra_context = extra_context or {}
		fileForm = FileFieldForm(request.POST, request.FILES)
		files = request.FILES.getlist('file_field')
		if fileForm.is_valid():
			for f in files:
				handle_uploaded_file(f)
				self.file_name = f.name
				self.file_lable = get_file_label(f)
		else:
			extra_context['my_form'] = FileFieldForm()
			self.file_name = ''
			self.file_lable = ''
		return super().change_view(
			request, object_id, form_url, extra_context=extra_context,
		)

	def add_view(self, request, form_url='', extra_context=None):
		extra_context = extra_context or {}
		fileForm = FileFieldForm(request.POST, request.FILES)
		files = request.FILES.getlist('file_field')
		if fileForm.is_valid():
			for f in files:
				handle_uploaded_file(f)
				self.file_name = f.name
				self.file_lable = get_file_label(f)
		else:
			extra_context['my_form'] = FileFieldForm()
			self.file_name = ''
			self.file_lable = ''
		return super().add_view(
			request, form_url, extra_context=extra_context,
		)

	def save_model(self, request, obj, form, change):
		if self.file_lable != '':
			'''after obj.save(), the obj.id will be updated'''
			obj.save()
			print("begin obj.id:", obj.id)
			p1 = r"--obj_id--"
			p1_pattern = re.compile(p1)
			p1_result = p1_pattern.sub(str(obj.id), self.file_lable)
			print(p1_result)
			obj.txt_body = obj.txt_body + "\n" + p1_result 
			move_file(obj.id, self.file_name)
		obj.save()


admin.site.register(Content, ContentAdmin)
admin.site.register(Author)
admin.site.register(Tag)
