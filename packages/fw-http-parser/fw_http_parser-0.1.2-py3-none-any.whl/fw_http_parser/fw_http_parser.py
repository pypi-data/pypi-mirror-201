import re


class HttpParser:

	def __init__(self, data):
		self.data = data

	def body(self):
		return re.search('({.+?})', self.data).group(0)

	def method(self):
		method = self.data.split(' ')[0]
		request_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
		return method if method in request_methods else None

	def host(self):
		return get_field('Host', self.data)

	def user_agent(self):
		return get_field('User-Agent', self.data)

	def content_type(self):
		return get_field('Content-Type', self.data)

	def get_field_by_name(self, name):
		return get_field(name, self.data)


def get_field(name, data) -> str | None:
	value = re.search(rf'{name}:\s(.+?)\s', data)
	return value.group(1) if value is not None else None
