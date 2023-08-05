import json

import requests
import typer

from launch.auth import cache
from launch.config import LaunchFlowConfig
from launch import constants
from launch import resources
from launch import utils

app = typer.Typer()

_END_POINT = 'flow'
_NAME_ARG = utils.get_name_arg(_END_POINT)


def _get_flow_name(name: str, org_name: str):
    if not org_name:
        config = LaunchFlowConfig.load()
        org_name = config.default_organization
        if not org_name:
            raise ValueError(
                '--name must be set or a default organization must be set in '
                'your config. You can set this with: `launch set-default-org '
                'myorg`')
    return f'{org_name}/{name}'


@app.command(help=utils.create_help_text(_END_POINT))
def create(
    name: str = _NAME_ARG,
    organization_name: str = constants.ORG_OPTION,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    flow_name = _get_flow_name(name, organization_name)
    resources.create(flow_name, _END_POINT, server_address)


@app.command(help=utils.get_help_text(_END_POINT))
def get(
    name: str = _NAME_ARG,
    organization_name: str = constants.ORG_OPTION,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    flow_name = _get_flow_name(name, organization_name)
    resources.get(flow_name,
                  endpoint=_END_POINT,
                  server_address=server_address)


@app.command(help=utils.get_add_reader_help(_END_POINT))
def add_reader(
    name: str = _NAME_ARG,
    organization_name: str = constants.ORG_OPTION,
    reader: str = constants.PERMISSION_ARG,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    flow_name = _get_flow_name(name, organization_name)
    resources.add_reader(name=flow_name,
                         reader=reader,
                         endpoint=_END_POINT,
                         server_address=server_address)


@app.command(help=utils.get_remove_reader_help(_END_POINT))
def remove_reader(
    name: str = _NAME_ARG,
    organization_name: str = constants.ORG_OPTION,
    reader: str = constants.PERMISSION_ARG,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    flow_name = _get_flow_name(name, organization_name)
    resources.remove_reader(name=flow_name,
                            reader=reader,
                            endpoint=_END_POINT,
                            server_address=server_address)


@app.command(help=utils.get_add_writer_help(_END_POINT))
def add_writer(
    name: str = _NAME_ARG,
    organization_name: str = constants.ORG_OPTION,
    writer: str = constants.PERMISSION_ARG,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    flow_name = _get_flow_name(name, organization_name)
    resources.add_writer(name=flow_name,
                         writer=writer,
                         endpoint=_END_POINT,
                         server_address=server_address)


@app.command(help=utils.get_remove_writer_help(_END_POINT))
def remove_writer(
    name: str = _NAME_ARG,
    organization_name: str = constants.ORG_OPTION,
    writer: str = constants.PERMISSION_ARG,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    flow_name = _get_flow_name(name, organization_name)
    resources.remove_writer(name=flow_name,
                            writer=writer,
                            endpoint=_END_POINT,
                            server_address=server_address)


_FLOW_NAME_HELP = 'The name of the deployed flow. If unset we will default to the same name as the flow file (e.g. main.py -> main-py).'  # noqa: E501


@app.command(help='Deploy a flow')
def deploy(
    flow_file: str = typer.Argument(
        ..., help='The python file containing your flow to deploy.'),
    name: str = typer.Option(default='', help=_FLOW_NAME_HELP),
    organization_name: str = constants.ORG_OPTION,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    if not name:
        name = flow_file.replace('.', '-')
    flow_name = _get_flow_name(name, organization_name)
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/deploy',
        headers={'Authorization': f'Bearer: {creds.id_token}'},
        data=json.dumps({'flow': flow_name}))

    if response.status_code != 200:
        raise ValueError(f'Deploy failed: {response.content.decode()}.')
