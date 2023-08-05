import unittest
from unittest import mock

import requests_mock
from typer.testing import CliRunner

from launch import cli


class CliTest(unittest.TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    @requests_mock.Mocker()
    @mock.patch('subprocess.Popen')
    def test_run(self, m: requests_mock.Mocker, popen_mock: mock.MagicMock):
        m.post('http://localhost:3569/submit_job')
        m.get('http://localhost:3569/get_job',
              response_list=[{
                  'json': {
                      'status': 'PENDING'
                  }
              }, {
                  'json': {
                      'status': 'RUNNING'
                  }
              }, {
                  'json': {
                      'status': 'FAILED'
                  }
              }])
        m.get('http://localhost:3569/get_job_logs',
              response_list=[{
                  'json': 'logs'
              }])
        result = self.runner.invoke(cli.app, [
            '--local', '-m', '--working-dir=/tmp/',
            '--requirements-file=/tmp/requirements.txt', '"main.py --my-flag"'
        ])
        self.assertEqual(0, result.exit_code, result.exception)

        # There should be 4 requests.
        # 1 for submiting the job
        # 3 for retrieving the job logs
        # 3 for checking the status of the job until completion
        self.assertEqual(len(m.request_history), 7)
        self.assertEqual(m.request_history[0].path, '/submit_job')
        self.assertEqual(m.request_history[1].path, '/get_job_logs')
        self.assertEqual(m.request_history[2].path, '/get_job')
        self.assertEqual(m.request_history[3].path, '/get_job_logs')
        self.assertEqual(m.request_history[4].path, '/get_job')
        self.assertEqual(m.request_history[5].path, '/get_job_logs')
        self.assertEqual(m.request_history[6].path, '/get_job')

        self.assertEqual(
            m.request_history[0].json(), {
                'entrypoint': 'python -m "main.py --my-flag"',
                'working_dir': '/tmp',
                'requirements_file': '/tmp/requirements.txt'
            })


if __name__ == '__main__':
    unittest.main()
