import json
import requests

import yaml

from launch.auth import cache


def create(name: str, endpoint: str, server_address: str):
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/{endpoint}/create?name={name}',
        headers={'Authorization': f'Bearer: {creds.id_token}'})

    if response.status_code != 200:
        json_content = json.loads(response.content.decode())
        raise ValueError(f'Create failed: {json_content["detail"]}.')


def get(
    name: str,
    endpoint: str,
    server_address: str,
    print_resource: bool = True,
):
    creds = cache.get_user_creds(server_address)
    response = requests.get(
        f'{server_address}/{endpoint}?name={name}',
        headers={'Authorization': f'Bearer: {creds.id_token}'})

    response_json = response.json()
    if print_resource:
        print(yaml.dump(response_json, sort_keys=False))
    return response_json


def add_permision(
    name: str,
    perm_to_add: str,
    permission: str,
    endpoint: str,
    server_address: str,
):
    resource = get(name, endpoint, server_address, print_resource=False)

    perms = resource[permission]
    if perm_to_add in perms:
        print(f'{perm_to_add} already has {permission} permission on: {name}')
        return
    perms.append(perm_to_add)

    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/{endpoint}/update?name={name}',
        headers={'Authorization': f'Bearer: {creds.id_token}'},
        data=json.dumps({permission: perms}))

    if response.status_code != 200:
        json_content = json.loads(response.content.decode())
        raise ValueError(f'Add failed: {json_content["detail"]}.')
    else:
        print(f'{perm_to_add} granted {permission} on: {name}.')


def add_reader(name: str, reader: str, endpoint: str, server_address: str):
    add_permision(name, reader, 'readers', endpoint, server_address)


def add_writer(name: str, writer: str, endpoint: str, server_address: str):
    add_permision(name, writer, 'writers', endpoint, server_address)


def remove_permision(
    name: str,
    perm_to_remove: str,
    permission: str,
    endpoint: str,
    server_address: str,
):
    resource = get(name, endpoint, server_address, print_resource=False)

    perms = resource[permission]
    if perm_to_remove not in perms:
        print(
            f'{perm_to_remove} does not have {permission} permission on: '
            f'{name}'
        )
        return
    perms.remove(perm_to_remove)

    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/{endpoint}/update?name={name}',
        headers={'Authorization': f'Bearer: {creds.id_token}'},
        data=json.dumps({permission: perms}))

    if response.status_code != 200:
        json_content = json.loads(response.content.decode())
        raise ValueError(f'Remove failed: {json_content["detail"]}.')
    else:
        print(f'{perm_to_remove} {permission} permission removed on: {name}')


def remove_reader(name: str, reader: str, endpoint: str, server_address: str):
    remove_permision(name, reader, 'readers', endpoint, server_address)


def remove_writer(name: str, writer: str, endpoint: str, server_address: str):
    remove_permision(name, writer, 'writers', endpoint, server_address)
