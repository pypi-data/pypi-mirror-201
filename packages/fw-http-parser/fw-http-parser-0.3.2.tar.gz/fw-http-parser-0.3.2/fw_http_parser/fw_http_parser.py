import re


class HttpParser:

	def __init__(self, data):
		self.data = data
		self._headers = []

	@property
	def body(self):
		body = re.search(r'({[\s\S]+?})', self.data)
		return body.group(0) if body is not None else None

	@property
	def method(self):
		method = self.data.split(' ')[0]
		request_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
		return method if method in request_methods else None

	@property
	def host(self):
		return get_field('Host', self.data)

	@property
	def user_agent(self):
		return get_field('User-Agent', self.data)

	@property
	def content_type(self):
		return get_field('Content-Type', self.data)

	@property
	def headers(self):
		idx = self.data.find("\r\n\r\n")
		lines = [line for line in self.data[:idx].split("\r\n")]

		while len(lines):
			curr = lines.pop(0)

			if curr.find(':') < 0:
				continue

			key, value = curr.split(':', 1)
			self._headers.append((key, value.strip()))

		return self._headers

	@property
	def route(self):
		return self.data.split(' ')[1]


def get_field(name, data) -> str | None:
	value = re.search(rf'{name}:\s(.+?)\s', data)
	return value.group(1) if value is not None else None
