from typing import Any
from typing import Dict

import aiohttp


async def request(
    hub,
    ctx,
    method: str,
    path: str,
    query_params: Dict[str, str] = {},
    data: Dict[str, Any] = {},
    headers: Dict[str, Any] = {},
):
    url = "/".join((ctx.acct.endpoint_url, path))
    async with aiohttp.ClientSession(
        loop=hub.pop.Loop, raise_for_status=True, auth=ctx.acct.auth
    ) as session:
        result = dict(ret=None, result=True, status=200, comment=[], headers={})

        if not headers.get("content-type"):
            headers["content-type"] = "application/json"

        async with session.request(
            url=url,
            method=method.lower(),
            allow_redirects=True,
            params=query_params,
            data=data,
        ) as response:
            result["status"] = response.status
            result["result"] = 200 <= response.status <= 204
            result["comment"].append(response.reason)
            result["headers"].update(response.headers)
            try:
                response.raise_for_status()
                result["ret"] = hub.tool.type.dict.namespaced(await response.json())
            except Exception as err:
                result["comment"].append(f"{err.__class__.__name__}: {err}")
                result["result"] = False
                ret = await response.read()
                result["ret"] = ret.decode() if hasattr(ret, "decode") else ret

            return result
