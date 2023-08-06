import os
import sqlite3

import requests

config = {
    'db': 'requests_cache.db',
    'dir': 'cache',
}


def write_database(url, etag, file):
    try:
        db_path = os.path.join(config['dir'], config['db'])
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS requests_etag(url PRIMARY KEY, etag, file)")
        cur.execute(f"INSERT OR REPLACE INTO requests_etag VALUES ('{url}', '{etag}', '{file}')")
        con.commit()
        con.close()
    except sqlite3.DatabaseError:
        pass


def read_database(url):
    try:
        db_path = os.path.join(config['dir'], config['db'])
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        res = cur.execute(f"SELECT etag, file FROM requests_etag WHERE url IS '{url}'")
        res = res.fetchone()
        con.close()
        if res is None:
            return None, None
        return res
    except sqlite3.DatabaseError:
        return None, None


def get(url, params=None, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    etag, file_path = read_database(url)
    headers = kwargs.pop('headers', {})
    if etag is not None:
        headers['If-None-Match'] = etag
    res = requests.get(url, params=params, headers=headers, **kwargs)
    if res.status_code == 304 and file_path is not None and os.path.isfile(file_path):
        with open(file_path, 'rb') as fp:
            res._content = fp.read()
        return res
    if res.ok and 'etag' in res.headers:
        try:
            file_path = url.replace(':', '_').replace('/', '_')
            file_path = os.path.join(config['dir'], file_path)
            os.makedirs(config['dir'], exist_ok=True)
            with open(file_path, 'wb') as fp:
                fp.write(res.content)
            write_database(url, res.headers['etag'], file_path)
        except OSError:
            pass
    return res
