from unittest import TestCase, mock
from os import environ

from src.cgiw.run import run

class TestRun(TestCase):
    @mock.patch.dict(environ, {
        'REQUEST_METHOD': 'GET'
    })
    def test_run_get(self):
        def handler(query, headers):
            return ({}, '')
        
        result = run(get=handler, verbose=False)
        self.assertEqual(result, '\n\n')

    @mock.patch.dict(environ, {
        'REQUEST_METHOD': 'POST'
    })
    def test_run_post(self):
        def handler(query, headers, body):
            return ({}, '')

        result = run(post=handler, verbose=False)
        self.assertEqual(result, '\n\n')