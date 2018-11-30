#encoding: utf-8

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import Content, Author
from django.conf import settings
from django.conf.urls.static import static
import os
import markdown2
import re
import hashlib
import lxml.etree as ET
from lxml import html
import urllib.request
import urllib.parse
import json
import accessToken
import cgi
import mqtt_control


# Create your views here.
class PageView(generic.DetailView):
	model = Content
	template_name = 'page/page.html'

	def get_object(self):
		object = super().get_object()
		object.txt_body = markdown2.markdown(object.txt_body)
		'''
		p1 = r"(<code>)([\s\S]+?)(</code>)"
		reg_pattern1 = re.compile(p1)
		def sub_cb(str1):
			return '%s%s%s' %(str1.group(1), cgi.escape(str1.group(2)), str1.group(3))
		object.txt_body = reg_pattern1.sub(sub_cb, object.txt_body)
		'''
		return object

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = FileFieldForm()
		return context 

	def post(self, request, *args, **kwargs):
		authorId =request.POST['author']
		fileForm = FileFieldForm(request.POST, request.FILES)
		files = request.FILES.getlist('file_field')
		if fileForm.is_valid():
			for f in files:
				FileFieldForm.handle_uploaded_file(fileForm, f)
			return HttpResponseRedirect(reverse('page:page', args=authorId))
		else:
			return HttpResponseRedirect(reverse('page:page', args=authorId))

class IndexView(generic.ListView):
	model = Content
	context_object_name = 'page_list'
	template_name = 'page/index.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['author_list'] = Author.objects.all().order_by('author')
		content_list = Content.objects.all().order_by('-txt_date')
		for item in content_list:
			item.txt_body = markdown2.markdown(item.txt_body)
			'''
			p1 = r">([^<>]+?)<"
			p2 = r"\n\n+"
			p1_result = ''
			reg_pattern = re.compile(p1)
			reg_pattern2 = re.compile(p2)
			for i in reg_pattern.findall(item.txt_body):
				tmp = reg_pattern2.sub("\n",i)
				p1_result += tmp # + " "
			item.txt_body = p1_result + " ..."
			'''
			root = ET.HTML(item.txt_body)
			p_lab = root.xpath('//p[1]')
			item.txt_body = p_lab[0].text
	
		context['content_list'] = content_list;
		return context

class AuthorView(generic.DetailView):
	model = Author
	template_name = 'page/author.html'

class WeChatView(generic.DetailView):
	model = Author
	template_name = 'page/author.html'

	def get(self, request, *args, **kwargs):
		try:
			signature = request.GET['signature']
			echostr = request.GET['echostr']
			timestamp = request.GET['timestamp']
			nonce = request.GET['nonce']
			token = "loupen"

			list1 = [token, timestamp, nonce]
			list1.sort()
			sha1 = hashlib.sha1()
			for i in list1:
				sha1.update(i.encode('utf-8'))
			hashcode = sha1.hexdigest()
			print("signature:" + signature)
			print("echostr:" + echostr)
			print("timestamp:" + timestamp)
			print("nonce:" + nonce)
			print("hashcode:" + hashcode)
		
			if hashcode == signature:
				return HttpResponse(echostr)
		except:
			return HttpResponse("error")

		return HttpResponse("error")

	def AddElement(self, root, tag, text, flag):
		tmp = ET.SubElement(root, tag)
		if flag == 0:
			tmp.text = text
		else:
			tmp.text = ET.CDATA(text)
	

	'''
	def post(self, request, *args, **kwargs):
		try:
			root = ET.fromstring(request.body)
			recv_to_user_name = root.find("ToUserName").text
			recv_from_user_name = root.find("FromUserName").text
			recv_create_time = root.find("CreateTime").text
			recv_msg_type = root.find("MsgType").text
			recv_msg_id = root.find("MsgId").text
			#print(recv_msg_type)
			if recv_msg_type == "text":
				recv_content = root.find("Content").text
			elif recv_msg_type == "image":
				recv_content = root.find("MediaId").text
				recv_pic_url = root.find("PicUrl").text
				print("pic_url", recv_pic_url)

			resp = ET.Element('xml')
			self.AddElement(resp, "ToUserName", recv_from_user_name, 1)
			self.AddElement(resp, "FromUserName", recv_to_user_name, 1)
			self.AddElement(resp, "CreateTime", recv_create_time, 0)
			self.AddElement(resp, "MsgType", recv_msg_type, 1)
			if recv_msg_type == "text":
				self.AddElement(resp, "Content", recv_content, 1)
			elif recv_msg_type == "image":
				image = ET.Element('Image')
				self.AddElement(image, "MediaId", recv_content, 1)
				resp.append(image)
			#print(ET.tostring(resp, encoding="unicode"))
			print("post pid: ", os.getpid(),"ppid: ", os.getppid(), "AccessToken: ", accessToken.GetAccessToken())

			return HttpResponse(ET.tostring(resp, encoding="unicode"))

		except:
			print("invalid wechat messages!")

		return HttpResponse("success")
	'''
class TianMaoView(generic.DetailView):
	model = Author
	template_name = 'page/author.html'
	dis_res = {
			"header": {
					"namespace": "AliGenie.Iot.Device.Discovery",
					"name": "DiscoveryDevicesResponse",
					"messageId": "ea426b7c-7d71-4421-bd9b-860617bd5ac8",
					"payLoadVersion": 1
			},
			"payload": {
					"devices": [{
							"deviceId": "34ea34cf2eff",
							"deviceName": "灯",
							"deviceType": "light",
							"zone": "",
							"brand": "",
							"model": "",
							"icon": "http://119.23.235.141/static/page/img/redmoon.jpg",
							"properties": [{
									"name": "powerstate",
									"value": "off"
							}],
							"actions": [
									"TurnOn",
									"TurnOff"
							],
							"extensions": {
									"extension1": "",
									"extension2": ""
							}
					}]
			}
	}
	con_res = {
			"header": {
					"namespace": "AliGenie.Iot.Device.Control",
					"name": "TurnOnResponse",
					"messageId": "ea426b7c-7d71-4421-bd9b-860617bd5ac8",
					"payLoadVersion": 1
			},
			"payload": {
					"deviceId": "34ea34cf2eff",
			}
	}

	def get(self, request, *args, **kwargs):
		print("get:"+request.body.decode("utf-8"))
		return HttpResponse("success")
		try:
			signature = request.GET['signature']
			echostr = request.GET['echostr']
			timestamp = request.GET['timestamp']
			nonce = request.GET['nonce']
			token = "loupen"

			list1 = [token, timestamp, nonce]
			list1.sort()
			sha1 = hashlib.sha1()
			for i in list1:
				sha1.update(i.encode('utf-8'))
			hashcode = sha1.hexdigest()
			print("signature:" + signature)
			print("echostr:" + echostr)
			print("timestamp:" + timestamp)
			print("nonce:" + nonce)
			print("hashcode:" + hashcode)
		
			if hashcode == signature:
				return HttpResponse(echostr)
		except:
			return HttpResponse("error")

		return HttpResponse("error")

	def AddElement(self, root, tag, text, flag):
		tmp = ET.SubElement(root, tag)
		if flag == 0:
			tmp.text = text
		else:
			tmp.text = ET.CDATA(text)
	

	def post(self, request, *args, **kwargs):
		print("post:"+request.body.decode("utf-8"))
		#try:
		req_data = json.loads(request.body.decode("utf-8"))
		req_namespace = req_data["header"]["namespace"] 
		req_name = req_data["header"]["name"] 
		req_msg_id = req_data["header"]["messageId"] 
		
		print("req_namespace:" + req_namespace)
		print("req_name:" + req_name)
		print("req_msg_id:" + req_msg_id)
		if req_namespace == "AliGenie.Iot.Device.Discovery":
			dis_res = self.dis_res
			dis_res["header"]["messageId"] = req_msg_id;
			print("return:" + str(dis_res))
			return HttpResponse(str(dis_res))
		elif req_namespace == "AliGenie.Iot.Device.Control":
			con_res = self.con_res
			con_res["header"]["name"] = req_name + "Response"
			con_res["header"]["messageId"] = req_msg_id;
			con_res["payload"]["deviceId"] = req_data["payload"]["deviceId"]
			print("return:" + str(con_res))
			ret = mqtt_control.SendControlMsg(req_name)
			if ret == "OK":
					print("mqtt send success!")
			else:
					print("mqtt send fail!")
			return HttpResponse(str(con_res))
		#except:
		print("invalid wechat messages!")

		return HttpResponse("success")
