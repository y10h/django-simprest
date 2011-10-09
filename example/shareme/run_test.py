import os
import json
import requests

HOST = 'http://127.0.0.1:8000/'


def test_connection():
    requests.get(HOST)


def test_doc():
    resp = requests.get(HOST)
    assert resp.status_code == 200
    assert resp.headers['content-type'] == 'text/plain'
    assert 'v1/files' in resp.content


def test_wrong_upload_method():
    resp = requests.put(HOST + 'v1/files')
    assert resp.status_code == 405


def test_wrong_upload_params_no_file():
    resp = requests.post(HOST + 'v1/files')
    assert resp.status_code == 400


def test_wrong_upload_params_several_files():
    resp = requests.post(HOST + 'v1/files',
                        files={'f1': open(__file__),
                               'f2': open(__file__)})
    assert resp.status_code == 400


def test_upload():
    resp = requests.post(HOST + 'v1/files',
                         files={'f1': open(__file__)})
    assert resp.status_code == 200
    assert HOST in resp.content


def test_upload_check_output_format():
    resp = requests.post(HOST + 'v1/files',
                         files={'some-name': open(__file__)})
    assert resp.headers['content-type'].startswith('application/json')
    data = json.loads(resp.content)
    assert list(sorted(data.keys())) == ['content_url', 'id', 'self_url',
                                         'title']
    assert data['title'] == 'some-name'
    fname = os.path.basename(__file__)
    assert data['content_url'].endswith(fname)
    assert str(data['id']) in data['self_url']


def test_upload_and_get_object():
    resp = requests.post(HOST + 'v1/files',
                         files={'f1': open(__file__)})
    assert resp.status_code == 200
    data = json.loads(resp.content)
    resp_get = requests.get(data['self_url'])
    assert resp_get.status_code == 200
    assert resp.headers['content-type'].startswith('application/json')
    data_get = json.loads(resp_get.content)
    assert data == data_get

def test_upload_and_get_content():
    resp = requests.post(HOST + 'v1/files',
                         files={'f1': open(__file__)})
    assert resp.status_code == 200
    data = json.loads(resp.content)
    resp_get = requests.get(data['content_url'])
    assert resp_get.status_code == 200

def test_upload_and_non_default_emitter():
    resp = requests.post(HOST + 'v1/files?format=xml',
                         files={'f1': open(__file__)})
    assert resp.status_code == 200
    assert resp.headers['content-type'].startswith('text/xml')
    assert resp.content.startswith('<?xml version="1.0"')

def run():
    import nose
    import sys

    args = [sys.argv[0], __file__] + sys.argv[1:]
    nose.run(argv=args)

if __name__ == '__main__':
    run()
