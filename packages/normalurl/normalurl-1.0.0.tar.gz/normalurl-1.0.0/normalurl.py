"""Convenient utility to parse and normalize urls."""

__version__ = "1.0.0"

from collections import namedtuple as _namedtuple
from typing import Union
from urllib.parse import urlparse as _urlparse, ParseResult

URL = _namedtuple('URL', 'scheme hostname port path query fragment netloc username password')


def _url_from_parse_result(result: ParseResult) -> URL:
	return URL(scheme=result.scheme or '', netloc=result.netloc or '', path=result.path or '', query=result.query or '', fragment=result.fragment or '', username=result.username or '', password=result.password or '', hostname=result.hostname or '', port=result.port or '')


URL.parse = _url_from_parse_result


def parse_url(url: str) -> URL:
	"""
	Parse url and return its elements structure.
	"""
	result = _urlparse(url)
	if not result.netloc and not result.scheme and not url.lstrip().startswith('//') or result.scheme and not url.lstrip().startswith(f'{result.scheme}://'):
		result = _urlparse(f'//{url}')
	return URL.parse(result)


def normalize_url(url: Union[str, URL, ParseResult], *, scheme: str = '', hostname: str = '', port: str = '', path: str = '', query: str = '', fragment: str = '', username: str = '', password: str = '') -> str:
	"""
	Ensure specified url elements are persist otherwise fill with default values.
	"""
	if isinstance(url, str):
		url = parse_url(url)
	elif isinstance(url, ParseResult):
		url = URL.parse(url)
	scheme = url.scheme or scheme
	if scheme:
		scheme += '://'
	username = url.username or username
	password = url.password or password
	if username and password:
		credentials = f'{username}:{password}'
	else:
		credentials = username or password
	hostname = url.hostname or hostname
	port = url.port or port
	if port:
		port = f':{port}'
	path = url.path or path
	query = url.query or query
	if query:
		query = f'?{query}'
	fragment = url.fragment or fragment
	if fragment:
		fragment = f'#{fragment}'
	return scheme + credentials + hostname + port + path + query + fragment


def parse_normalized_url(url: Union[str, ParseResult], *, scheme: str = '', hostname: str = '', port: str = '', path: str = '', query: str = '', fragment: str = '', username: str = '', password: str = '') -> URL:
	"""
	Ensure specified url elements are persist otherwise fill with default values. Then parse url and return its elements structure.
	"""
	return parse_url(normalize_url(url, scheme=scheme, hostname=hostname, port=port, path=path, query=query, fragment=fragment, username=username, password=password))
