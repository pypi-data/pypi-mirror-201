# Normal URL

Convenient utility to parse and normalize urls.

```python
from normalurl import *

print(parse_url('localhost'))
print(parse_url('localhost:12345'))
print(normalize_url('localhost', scheme='http', port='1122'))
print(parse_normalized_url('localhost:12345', scheme='http', port='1122'))
```

> URL(scheme='', hostname='localhost', port='', path='', query='', fragment='', netloc='localhost', username='', password='')  
> URL(scheme='', hostname='localhost', port=12345, path='', query='', fragment='', netloc='localhost:12345', username='', password='')  
> http://localhost:1122  
> URL(scheme='http', hostname='localhost', port=12345, path='', query='', fragment='', netloc='localhost:12345', username='', password='')

# Usage

### Normalize URL

Function `normalize_url(url: Union[str, URL, ParseResult], *, scheme: str = '', hostname: str = '', port: str = '', path: str = '', query: str = '', fragment: str = '', username: str = '', password: str = '') -> str` ensures each element of url has non-empy value otherwise sets default one.

Just do nothing:

```python
print(normalize_url('localhost'))
```

> localhost

Ensure url describes scheme and port. If not persist user *http* scheme and port *1122*.

```python
print(normalize_url('localhost', scheme='http', port='1122'))
print(normalize_url('https://localhost', scheme='http', port='1122'))
print(normalize_url('localhost:12345', scheme='http', port='1122'))
print(normalize_url('https://localhost:12345', scheme='http', port='1122'))
```

> http://localhost:1122  
> https://localhost:1122  
> http://localhost:12345  
> https://localhost:12345

### Parse URL

Function `parse_url(url: str) -> URL` parse url elements in named tuple structure `URL`. Default value for each element is empty string `''`.

Parsed elements are:

* scheme
* hostname
* port
* path
* query
* fragment
* netloc
* username
* password

```python
print(parse_url('localhost'))
print(parse_url('localhost:12345'))
print(parse_url('http://example.org'))
print(parse_url('https://example.org:8080/user/search?name=Bob&age=30#profile'))
print(parse_url('https://admin:123@example.org:8080/user/search?name=Bob&age=30#profile'))
```

> URL(scheme='', hostname='localhost', port='', path='', query='', fragment='', netloc='localhost', username='', password='')  
> URL(scheme='', hostname='localhost', port=12345, path='', query='', fragment='', netloc='localhost:12345', username='', password='')  
> URL(scheme='http', hostname='example.org', port='', path='', query='', fragment='', netloc='example.org', username='', password='')  
> URL(scheme='https', hostname='example.org', port=8080, path='/user/search', query='name=Bob&age=30', fragment='profile', netloc='example.org:8080', username='', password='')  
> URL(scheme='https', hostname='example.org', port=8080, path='/user/search', query='name=Bob&age=30', fragment='profile', netloc='admin:123@example.org:8080', username='admin', password='123')

### Parse normalized URL

Function `parse_normalized_url(url: Union[str, ParseResult], *, scheme: str = '', hostname: str = '', port: str = '', path: str = '', query: str = '', fragment: str = '', username: str = '', password: str = '') -> URL` works exactly like `normalize_url` + `parse_url` - normalizes url then parses it.

Ensure url describes scheme and port. If not persist user *http* scheme and port *1122*.

```python
print(parse_normalized_url('localhost', scheme='http', port='1122'))
print(parse_normalized_url('https://localhost', scheme='http', port='1122'))
print(parse_normalized_url('localhost:12345', scheme='http', port='1122'))
print(parse_normalized_url('https://localhost:12345', scheme='http', port='1122'))
```

> URL(scheme='http', hostname='localhost', port=1122, path='', query='', fragment='', netloc='localhost:1122', username='', password='')  
> URL(scheme='https', hostname='localhost', port=1122, path='', query='', fragment='', netloc='localhost:1122', username='', password='')  
> URL(scheme='http', hostname='localhost', port=12345, path='', query='', fragment='', netloc='localhost:12345', username='', password='')  
> URL(scheme='https', hostname='localhost', port=12345, path='', query='', fragment='', netloc='localhost:12345', username='', password='')

# Why not just use urllib?

Because urlib does not cover some common edge cases.

Just rewrite the first example with urllib:

```python
from urllib.parse import urlparse

print(urlparse('localhost'))
print(urlparse('localhost:12345'))
```

> ParseResult(scheme='', netloc='', path='localhost', params='', query='', fragment='')  
> ParseResult(scheme='localhost', netloc='', path='12345', params='', query='', fragment='')

As you can see, urllib considers localhost as path while it is actually hostname.
Moreover,  *\<host\>:\<port\>* are parsed as scheme (like http) for localhost and path for port which is absolutely wrong.
