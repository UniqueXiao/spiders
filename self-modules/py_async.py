#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python 异步编程

import socket
import datetime
from concurrent import futures
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


#1 阻塞方式
def blocking_way():
	sock = socket.socket()
	sock.connect(('example.com', 80))
	
	request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
	sock.send(request.encode('ascii'))
	response = b''
	chunk = sock.recv(4096)
	while chunk:
		response += chunk
		chunk = sock.recv(4096)
		
	return response

	
#1.1 同步阻塞方式  耗时6.61s
def sync_way():    
	res = []
	for i in range(10):
		res.append(blocking_way())
		
	return len(res)

	
#1.2 多进程方式
def process_way():
	workers = 10
	with futures.ProcessPoolExecutor(workers) as executor:
		futs = {executor.submit(blocking_way) for i in range(10)}	
	return len([fut.result() for fut in futs])

	
#1.3 多线程方式  耗时1.76s
def thread_way():
	workers = 10
	with futures.ThreadPoolExecutor(workers) as executor:
		futs = {executor.submit(blocking_way) for i in range(10)}
	return len([fut.result() for fut in futs])
	

# start = datetime.datetime.now()
# l = sync_way()
# end = datetime.datetime.now()
# print(l)
# print((end-start))

	
#2 非阻塞方式

#2.1 最原始非阻塞方式 异步IO+try+轮询  耗时5.16s
def nonblocking_way():
	sock = socket.socket()
	sock.setblocking(False)
	
	try:
		sock.connect(('example.com', 80))
	except BlockingIOError:
		# 非阻塞连接过程中会抛出异常
		pass
	request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
	data = request.encode('ascii')
	#不知道socket何时就绪，所以不断尝试发送
	while True:
		try:
			sock.send(data)
			#直到send不抛出异常，则发送完成
			break
		except OSError:
			pass
			
	response = b''
	while True:
		try:
			chunk = sock.recv(4096)
			while chunk:
				response += chunk
				chunk = sock.recv(4096)
			break
		except OSError:
			pass
			
	return response
	
def sync_way():    
	res = []
	for i in range(10):
		res.append(nonblocking_way())
		
	return len(res)
	
# start = datetime.datetime.now()
# l = sync_way()
# end = datetime.datetime.now()
# print(l)
# print((end-start))

		
#3 非阻塞改进

#3.1 selectors与回调(callback)、事件循环(Event Loop)    耗时3.42s
selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9',}
class Crawler:
	def __init__(self, url):
		self.url = url
		self.sock = None
		self.response = b''
		
	def fetch(self):
		self.sock = socket.socket()
		self.sock.setblocking(False)
		try:
			self.sock.connect(('example.com', 80))
		except BlockingIOError:
			pass
		selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)
		
	def connected(self, key, mask):
		selector.unregister(key.fd)
		get = 'GET {0} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
		self.sock.send(get.encode('ascii'))
		selector.register(key.fd, EVENT_READ, self.read_response)
		
	def read_response(self, key, mask):
		global stopped
		#如果响应大于4KB,下一次循环会继续
		chunk = self.sock.recv(4096)
		if chunk:
			self.response += chunk
		else:
			selector.unregister(key.fd)
			urls_todo.remove(self.url)
			if not urls_todo:
				stopped = True

def loop():
	while not stopped:
		#阻塞 直到一个事件发生
		events = selector.select()
		for event_key, event_mask in events:
			callback = event_key.data
			callback(event_key, event_mask)

# if __name__ == '__main__':
	# import time
	# start = time.time()
	# for url in urls_todo:
		# crawler = Crawler(url)
		# crawler.fetch()
	# loop()
	# print(time.time() - start)

	
	

# 4 基于生成器的协程  耗时3.5s

selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9',}

# 未来对象(Future)
class Future:
	def __init__(self):
		self.result = None
		self._callbacks = []
	
	def add_done_callback(self, fn):
		self._callbacks.append(fn)
		
	def set_result(self, result):
		self.result = result
		for fn in self._callbacks:
			fn(self)
			
#重构Crawler
class Crawler:
	def __init__(self, url):
		self.url = url
		self.response = b''
		
	def fetch(self):
		sock = socket.socket()
		sock.setblocking(False)
		try:
			sock.connect(('example.com', 80))
		except BlockingIOError:
			pass
		f = Future()
		
		def on_connected():
			f.set_result(None)
			
		selector.register(sock.fileno(), EVENT_WRITE, on_connected)
		yield f
		selector.unregister(sock.fileno())
		get = 'GET {0} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
		sock.send(get.encode('ascii'))
		
		global stopped
		while True:
			f = Future()
			
			def on_readable():
				f.set_result(sock.recv(4096))
				
			selector.register(sock.fileno(), EVENT_READ, on_readable)
			chunk = yield f
			selector.unregister(sock.fileno())
			if chunk:
				self.response += chunk
			else:
				urls_todo.remove(self.url)
				if not urls_todo:
					stopped = True
				break
				
class Task:
	def __init__(self, coro):
		self.coro = coro
		f = Future()
		f.set_result(None)
		self.step(f)
		
	def step(self, future):
		try:
			# send会进入到coro执行， 即fetch, 直到下次yield
			# next_future 为yield返回的对象
			next_future = self.coro.send(future.result)
		except StopIteration:
			return
		next_future.add_done_callback(self.step)
		
def loop():
	while not stopped:
		events = selector.select()
		for event_key, event_mask in events:
			callback = event_key.data
			callback()
			
if __name__ == '__main__':
	import time
	start = time.time()
	for url in urls_todo:
		crawler = Crawler(url)
		Task(crawler.fetch())
	loop()
	print(time.time() - start)




# 5 用yield from改进生成器协程




	
# 6 asyncio和协程  耗时1.55s
import aiohttp
import asyncio

host = 'http://www.example.com'
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9',}

loop = asyncio.get_event_loop()

async def fetch(url):
	async with aiohttp.ClientSession(loop=loop) as session:
		async with session.get(url) as response:
			response = await response.read()
			return response

# if __name__ == '__main__':
	# import time
	# start = time.time()
	# tasks = [fetch(host + url ) for url in urls_todo]
	# loop.run_until_complete(asyncio.gather(*tasks))
	# print(time.time() - start)
	
	
	
