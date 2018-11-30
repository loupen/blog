import threading,urllib.request,json
import time,signal,sys,os
import socket,select
import paho.mqtt.publish as publish

class Socket(threading.Thread):
	def __init__(self):
		super().__init__()
	def run(self):
		sk_path = "/tmp/MqttToken.sock"
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
						publish.single("lp", data.decode(), hostname="127.0.0.1")
						print("published ok!")
						fd.sendall(b"OK")
					except ConnectionResetError:
						print("connect error")
					finally:
						recv_list.remove(fd)
						fd.close()
			for fd in error_list:
				print("error:", fd)
		sk.close()
				
def SendControlMsg(msg):
	sk_path = "/tmp/MqttToken.sock"
	sk = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	ret = "FAIL"

	try:
		sk.connect(sk_path)
	except socket.error as e:
		print(e)
		return 0;
	try:
		print("sk send0:" + msg)
		sk.sendall(str.encode(msg))
		data = sk.recv(1024)
		#success should return "OK"
		ret = data.decode()
		print("sk:" + ret)
		#print(access_token)
	except socket.error as e:
		print(e)
	finally:
		sk.shutdown(socket.SHUT_RDWR)
		sk.close()
		return ret

def quit(signum, frame):
	print("Main Thread exit")
	sys.exit()

def CreateThread():
	#signal.signal(signal.SIGINT, quit)
	#signal.signal(signal.SIGTERM, quit)

	t1 = Socket()
	t1.setDaemon(True)
	t1.start()
