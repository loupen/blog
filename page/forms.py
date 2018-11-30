from django import forms
from django.conf import settings
import os
from datetime import datetime
import shutil

class FileFieldForm(forms.Form):
	file_field = forms.FileField(label="Upload File:")

def get_file_label(f):
	name = f.name
	path = settings.STATIC_URL + "page/--obj_id--/"
	#path = os.path.join(settings.MEDIA_URL, "page/")
	pathName = path + name
	ext0 = os.path.splitext(name)[0].lower()
	ext1 = os.path.splitext(name)[1].lower()
	img_ext = ['.png','.jpg','.gif',]
	video_ext = ['.mov','.f4v','.flv','.3gp','.aac','.wav','.mp4','.mp3','.ogg','.avi']
	label = ''
	if ext1 in img_ext:
		label = '\n<div width="100%" height="480px">\n' + \
				'<img src="' + pathName + '" ' + 'style="width:100%;" alt="lost"/>\n' +\
				'</div>\n'
	elif ext1 in video_ext:
		'''
		label = '\n<div id="' + ext0 + '" ' + 'width="100%" height="480px"> Loading the player... </div>\n' + \
				'<script>\n' + \
				'	jwplayer("' + ext0 + '")' + '.setup({\n' + \
				'		file:"' + pathName + '",\n' + \
				'	});\n' + \
				'</script>\n'
		'''
		label = '\n<video class="video-js" controls preload="auto">\n' + \
				'	<source src="' + pathName + '"' + ' type="video/mp4">\n' + \
				'</video>\n'

	pathName = settings.BASE_DIR + pathName
	print(pathName)
	print(label)
	return label

def handle_uploaded_file(f):
	file_path = "/tmp/" + f.name
	if os.path.exists(file_path):
		os.unlink(file_path)
	try:
		with open(file_path, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
	except:
		print("write file error")

def move_file(obj_id, file_name):
	old_path = "/tmp/" + file_name
	new_path = settings.BASE_DIR + settings.STATIC_URL + "page/" + str(obj_id) + "/"
	print("new path: ", new_path)
	if os.path.exists(old_path):
		if not os.path.exists(new_path):
			os.makedirs(new_path)
		shutil.move(old_path, new_path + file_name)

def delete_file(obj_id):
	path = settings.BASE_DIR + settings.STATIC_URL + "page/" + str(obj_id) + "/"
	print("rm path: ", path)
	if os.path.exists(path):
		shutil.rmtree(path)
