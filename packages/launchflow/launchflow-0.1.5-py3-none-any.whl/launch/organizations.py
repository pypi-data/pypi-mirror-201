import typer

from launch.config import LaunchFlowConfig
from launch import constants
from launch import resources
from launch import utils

app = typer.Typer()

_END_POINT = 'organization'
_NAME_ARG = utils.get_name_arg(_END_POINT)


def _get_org_name(name: str):
    if not name:
        config = LaunchFlowConfig.load()
        name = config.default_organization
        if not name:
            raise ValueError(
                '--name must be set or a default organization must be set in '
                'your config. You can set this with: `launch set-default-org '
                'myorg`')
    return name


@app.command(help=utils.create_help_text(_END_POINT))
def create(
    name: str = _NAME_ARG,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    resources.create(name, _END_POINT, server_address)


@app.command(help=utils.get_help_text(_END_POINT))
def get(
    name: str = constants.ORG_OPTION,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    name = _get_org_name(name)
    resources.get(name, endpoint=_END_POINT, server_address=server_address)


@app.command(help=utils.get_add_reader_help(_END_POINT))
def add_reader(name: str = constants.ORG_OPTION,
               reader: str = constants.PERMISSION_ARG,
               server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.add_reader(name=name,
                         reader=reader,
                         endpoint=_END_POINT,
                         server_address=server_address)


@app.command(help=utils.get_remove_reader_help(_END_POINT))
def remove_reader(name: str = constants.ORG_OPTION,
                  reader: str = constants.PERMISSION_ARG,
                  server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.remove_reader(name=name,
                            reader=reader,
                            endpoint=_END_POINT,
                            server_address=server_address)


@app.command(help=utils.get_add_writer_help(_END_POINT))
def add_writer(name: str = constants.ORG_OPTION,
               writer: str = constants.PERMISSION_ARG,
               server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.add_writer(name=name,
                         writer=writer,
                         endpoint=_END_POINT,
                         server_address=server_address)


@app.command(help=utils.get_remove_writer_help(_END_POINT))
def remove_writer(name: str = constants.ORG_OPTION,
                  writer: str = constants.PERMISSION_ARG,
                  server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.remove_writer(name=name,
                            writer=writer,
                            endpoint=_END_POINT,
                            server_address=server_address)


@app.command(help='Adds a flow creator to an organization')
def add_flow_creator(name: str = constants.ORG_OPTION,
                     flow_creator: str = constants.PERMISSION_ARG,
                     server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.add_permision(name=name,
                            perm_to_add=flow_creator,
                            permission='flow_creators',
                            endpoint=_END_POINT,
                            server_address=server_address)


@app.command(help='Removes a flow creator from an organization')
def remove_flow_creator(name: str = constants.ORG_OPTION,
                        flow_creator: str = constants.PERMISSION_ARG,
                        server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.remove_permision(name=name,
                               perm_to_remove=flow_creator,
                               permission='flow_creators',
                               endpoint=_END_POINT,
                               server_address=server_address)
