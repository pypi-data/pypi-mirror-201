
import json
from typing import Coroutine
from functools import wraps
from aiohttp import web
from json import JSONEncoder, JSONDecoder
from aiofauna.json import parse_json_or_none
from jinja2 import Environment, FileSystemLoader, Template

class AioEncoder(JSONEncoder):
    async def default(self, o):
        if isinstance(o, web.Request):
            try:
                return json.dumps(json.loads((await o.content.read()).decode("utf-8")))
            except:
                return json.dumps(await o.json())
        elif isinstance(o, web.Response):
            return json.dumps(o.body)


class AioDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self._object_hook, *args, **kwargs)

    def _object_hook(self, obj):
        return obj

    def decode(self, s, _w=parse_json_or_none):
        return super().decode(s)


def jsonify(func):
    @wraps(func)
    async def wrapper(request):
        try:
            return web.json_response(await func(request))
        except Exception as e:
            return web.json_response(func(request))
    return wrapper


def redirect(url):
    return web.HTTPFound(url)


def make_response(data, headers=None, status=200):
    return web.Response(body=data, headers=headers, status=status)


def render_template(template_name, **kwargs):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name).render(**kwargs)
    return web.Response(body=template.encode("utf-8"), content_type="text/html")