import typer

from launch import constants


def _get_help_str(endpoint: str):
    # If the endpoint starts with a vowel we want it to say:
    #    an {endpoint}
    if endpoint.lower()[0] in 'aeiou':
        return f'n {endpoint}'
    else:
        return f' {endpoint}'


def get_name_arg(endpoint: str):
    return typer.Argument(
        ...,
        help=constants.NAME_HELP_TEXT.format(endpoint),
        show_default=False)


def get_add_reader_help(endpoint: str):
    return constants.ADD_READER_HELP_TEXT.format(_get_help_str(endpoint))


def get_remove_reader_help(endpoint: str):
    return constants.REMOVE_READER_HELP_TEXT.format(_get_help_str(endpoint))


def get_add_writer_help(endpoint: str):
    return constants.ADD_WRITER_HELP_TEXT.format(_get_help_str(endpoint))


def get_remove_writer_help(endpoint: str):
    return constants.REMOVE_WRITER_HELP_TEXT.format(_get_help_str(endpoint))


def get_help_text(endpoint: str):
    return constants.GET_HELP_TEXT.format(_get_help_str(endpoint))


def create_help_text(endpoint: str):
    return constants.CREATE_HELP_TEXT.format(_get_help_str(endpoint))
