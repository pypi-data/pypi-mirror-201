# requests-etag

Wrapper over requests package to support etag caching by default

## Install

```
pip install requests-etag
```

## Usage

```python
>>> import requests_etag
>>> res = requests_etag.get('https://example.com/')
>>> res.status_code
200
>>> len(res.text)
1527903
>>> res = requests_etag.get('https://example.com/') # cached
>>> res.status_code
304
>>> len(res.text)
1527903
```

## Configuration

```python
import requests_etag

requests_etag.config['dir'] = 'mycache'
requests_etag.config['db'] = 'db.sqlite3'
```
