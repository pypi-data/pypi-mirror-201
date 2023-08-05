import os
import signal
import subprocess
from sys import platform
from dataclasses import dataclass
from pkg_resources import resource_filename
from typing import Dict, Optional

import requests
import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ray.job_submission import JobSubmissionClient

RAY_CLUSTER_ADDRESS = 'http://127.0.0.1:8265'
PROMETHEUS = 'http://localhost:9090/'


@dataclass
class SourceInfo:
    file_path: str


@dataclass
class JobInfo:
    job_id: str
    status: str
    source_id: str
    sink_id: str
    metrics: Dict[str, str]
    source_info: SourceInfo


@dataclass
class RunnerState:
    job_info: Optional[JobInfo] = None
    ray_cluster_address: Optional[str] = None
    prometheus_address: Optional[str] = None


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.state.runner = RunnerState()

prometheus_process = None

job_id = None


def get_job_id():
    global job_id
    if job_id is None:
        raise fastapi.HTTPException(
            400, 'no job has been started on the server yet.')
    return job_id


@app.on_event("startup")
def startup():
    global prometheus_process
    subprocess.run('ray start --head', shell=True)
    # TODO: should include other distributions.
    prom_dir = resource_filename('launch', 'prometheus')
    if platform == "linux" or platform == "linux2":
        executable = 'linux/prometheus'
    elif platform == "darwin":
        executable = 'mac/prometheus'
    else:
        raise ValueError(
            f'launch CLI is not supported for platform: {platform}')
    prometheus_process = subprocess.Popen(
        f'./{executable} --config.file=/tmp/ray/session_latest/metrics/prometheus/prometheus.yml',  # noqa
        cwd=f'{prom_dir}/.',
        shell=True)


@app.on_event("shutdown")
def shutdown():
    global prometheus_process
    subprocess.run('ray stop', shell=True)
    prometheus_process.terminate()
    prometheus_process.wait()


class JobSubmission(BaseModel):
    entrypoint: str
    working_dir: str
    requirements_file: str


@app.post('/submit_job')
async def submit_job(submission: JobSubmission):
    global job_id
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)

    if job_id is not None:
        job_info = client.get_job_info(job_id)
        if job_info.status in ['RUNNING', 'PENDING']:
            raise fastapi.HTTPException(
                400,
                'job already running, please cancel job or wait for it to '
                'finish.')
        job_id = None
    request = {'entrypoint': submission.entrypoint}
    runtime_env = {}
    if submission.working_dir:
        runtime_env['working_dir'] = submission.working_dir
    if submission.requirements_file:
        runtime_env['pip'] = submission.requirements_file
    if runtime_env:
        request['runtime_env'] = runtime_env
    job_id = client.submit_job(**request)


def get_prometheus_metrics(metric, fn):
    query = f'ray_{metric}'
    if fn is not None:
        query = f'{fn}({query})'
    response = requests.get(PROMETHEUS + '/api/v1/query',
                            params={
                                'query': query
                            }).json()
    if response.get('status') == 'success':
        try:
            return response.get('data').get('result')[0].get('value')[1]
        except Exception:
            return None


@app.get('/get_job')
async def get_job():
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    current_job_id = get_job_id()
    job_info = client.get_job_info(current_job_id)
    job_info.metadata['throughput'] = 'N/A'
    job_info.metadata['num_replicas'] = 'N/A'
    job_info.metadata['process_time'] = 'N/A'
    for metric, fn in [('num_replicas', None), ('process_time', 'avg'),
                       ('throughput', 'sum')]:
        prom_metric = get_prometheus_metrics(metric, fn)
        if prom_metric is not None:
            job_info.metadata[metric] = prom_metric
    return job_info


@app.get('/stop_job')
async def stop_job():
    current_job_id = get_job_id()
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    return client.stop_job(current_job_id)


last_log_return = 0


@app.get('/get_job_logs')
async def get_job_logs():
    global last_log_return
    current_job_id = get_job_id()
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    logs = client.get_job_logs(current_job_id)
    to_ret_logs = logs[last_log_return:]
    last_log_return = len(logs)
    return to_ret_logs


@app.get('/drain_job')
async def drain_job():
    current_job_id = get_job_id()
    client = JobSubmissionClient(RAY_CLUSTER_ADDRESS)
    job_info = client.get_job_info(current_job_id)
    pid = job_info.driver_info.pid
    print('PID: ', pid)
    os.kill(int(pid), signal.SIGINT)
    return True
