import pathlib

import requests


def context(hub, ctx, directory: pathlib.Path):
    swagger = hub.pop_create.openapi3.init.read(source=hub.OPT.pop_create.specification)

    # Convert swagger to openapi3
    response = requests.post(
        "https://converter.swagger.io/api/convert",
        json=dict(swagger),
        headers={"Content-Type": "application/json"},
    )
    ctx.specification = response.json()

    # get ctx from openapi3 with changes that turn swagger into openapi3
    hub.pop_create.init.run(directory=directory, subparsers=["openapi3"], **ctx)

    return ctx
