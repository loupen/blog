import threading,urllib.request,json
import time,signal,sys,os
import socket,select

global access_token
access_token = ''

class AccessToken(threading.Thread):
	def __init__(self):
		super().__init__()
		self.left_time = 0

	def run(self):
		global access_token
		while True:
			if self.left_time < 10:
				print("left_time is less than 10")
				'''you need to replace appid and secret with your own'''
				params = urllib.parse.urlencode({'grant_type':'client_credential', 'appid':'xxxxxx', 'secret':'xxxxxx'})
				url = "https://api.weixin.qq.com/cgi-bin/token?%s" % params
				try:
					url_response = urllib.request.urlopen(url)
					result = json.loads(url_response.read().decode('utf-8'))
					access_token = result['access_token']
					self.left_time = result['expires_in']
					print("server update token")
				except:
					print("invalid token!")

			if self.left_time > 2:
				self.left_time -= 2
				#print("left_time is ", self.left_time, " pid:", os.getpid(), "ppid:", os.getppid())
			time.sleep(2)

class Socket(threading.Thread):
	def __init__(self):
		super().__init__()
	def run(self):
		global access_token
		sk_path = "/tmp/token.sock"
		sk = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		if os.path.exists(sk_path):
			os.unlink(sk_path)
		sk.bind(sk_path)
		sk.listen(5)
		sk.setblocking(False)

		recv_list = [sk,]
		while True:
			read_list, write_list, error_list = select.select(recv_list, [], recv_list, 5)

			for fd in read_list:
				if fd == sk:
					conn, addr = fd.accept()
					recv_list.append(conn)
					print("append connection addr:", addr)
					print("socket pid:", os.getpid(), "ppid:", os.getppid())
					print(recv_list)
				else:
					try:
						data = fd.recv(1024)
						if data.decode() == 'g':
							print("return token")
							fd.sendall(str.encode(access_token))
					except ConnectionResetError:
						print("connect error")
					finally:
						recv_list.remove(fd)
						fd.close()
			for fd in error_list:
				print("error:", fd)
		sk.close()
				
def GetAccessToken():
	sk_path = "/tmp/token.sock"
	sk = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	try:
		sk.connect(sk_path)
	except socket.error as e:
		print(e)
		return 0;
	try:
		msg = b'g'
		sk.sendall(msg)
		data = sk.recv(1024)
		print(data)
		access_token = data.decode()
		#print(access_token)
	except socket.error as e:
		print(e)
	finally:
		sk.shutdown(socket.SHUT_RDWR)
		sk.close()
		return access_token

def quit(signum, frame):
	print("Main Thread exit")
	sys.exit()

def CreateThread():
	#signal.signal(signal.SIGINT, quit)
	#signal.signal(signal.SIGTERM, quit)

	t1 = AccessToken()
	t2 = Socket()
	t1.setDaemon(True)
	t2.setDaemon(True)
	t1.start()
	t2.start()
	
