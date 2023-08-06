#!/usr/bin/env python3

import logging
import json_fix
import json
import string

import dojo



def expand_data(data, template):

    """

    :param data:
    :return:
    """

    expanded_data = None
    expanded_template = dict()

    for tk, tv in template:
        expanded_template[tk] = json.dumps(tv)

    if isinstance(data, dict):
        expanded_data = dict()
        for k, v in data.items():
            if isinstance(v, (list, tuple)):
                expanded_data[k] = [expand_data(vi, template) for vi in v]
            else:
                expanded_data[k] = expand_data(v, template)

    elif isinstance(data, string.Template):
        expanded_data = data.safe_substitute(**expanded_template)
    else:
        expanded_data = data

    return expanded_data

def write_chain(chain=[], **kwargs):
    '''
    Write this chain of objects
    :param chain:
    :return:
    '''

    logger = logging.getLogger("dojo.write_chain")

    host = kwargs.get("host", None)
    token = kwargs.get("token", None)
    username = kwargs.get("username", None)
    password = kwargs.get("password", None)

    log = []

    if host is None:
        logger.error("Write chain needs a defectDojo host specified in Host to work")
        raise ValueError("No Host")
    if token is None and (username is None or password is None):
        logger.error("Application needs either a username/password combination or an api token specified")
        raise ValueError("No Authentication")

    all_args = {"host": host,
                "token": token,
                "username": username,
                "password": password}

    template_obj = None
    if chain is not None:
        template_obj = {}
        for x in range(0, len(chain)):
            # Search for Chain Item
            tdata = expand_data(chain[x]["data"], template_obj)

            dojo_obj = chain[x]["type"](
                action="search",
                data=chain[x]["search_data"]
                **all_args)

            if dojo_obj.id is None:
                # None found create new Object
                dojo_obj.data = tdata
                dojo_obj.new_obj()
            else:
                # One Found Update Existing Object
                dojo_obj.update_obj(tdata)

            template_obj[x] = dojo_obj
    else:
        logger.warning("No Chain of Items Given")

    return template_obj
