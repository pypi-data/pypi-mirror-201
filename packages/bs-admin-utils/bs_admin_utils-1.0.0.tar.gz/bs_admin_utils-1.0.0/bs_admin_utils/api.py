from asyncio import get_running_loop
from beanie.odm.queries.find import FindMany
from blacksheep import file, Request
from blacksheep.server.controllers import APIController, delete, get, patch, post, put, ws
from blacksheep.server.responses import not_found
from kikiutils.aiofile import aread_file
from kikiutils.check import isbytes, isfile
from kikiutils.file import get_file_mime, save_file_as_bytesio
from kikiutils.json import dict_key_camel_to_snake, dict_key_snake_to_camel
from pathlib import Path
from PIL.Image import Image
from typing import Optional, Type

from .model import BaseModel


ModelType = Type[BaseModel]


class BaseAPIController(APIController):
    base_url: str = '/api'
    loop = get_running_loop()
    model: ModelType
    success = 'success'
    to_dict_excludes = {}
    to_dict_includes = {}

    # Data process and route url

    @classmethod
    def route(cls):
        return cls.base_url

    async def model_to_dict(self, model: ModelType, is_link: bool = False):
        if is_link:
            model = await model.fetch()

        data = model.dict(
            exclude=self.to_dict_excludes or None,
            include=self.to_dict_includes or None
        )

        await self.process_data(data, model)
        data['id'] = str(model.id)
        return dict_key_snake_to_camel(data)

    async def models_to_data(self, models: FindMany[ModelType]):
        return {
            'count': await models.count(),
            'data': [
                await self.model_to_dict(model)
                async for model in models
            ]
        }

    async def process_data(self, data: dict[str], model: ModelType):
        pass

    # Apis

    async def delete(self, id: str):
        if model := await self.model.from_id(id):
            await model.delete()
            return self.success
        return self.error()

    async def get_list(self, rq: Request, fetch_links: bool = True, with_children: bool = True):
        skip, limit = get_data_range(rq)
        models = self.model.find(
            fetch_links=fetch_links,
            limit=limit,
            skip=skip,
            with_children=with_children
        )

        return await self.models_to_data(models)

    async def save(self, data: dict, id: str = ''):
        await self.model.update_or_create(id, **data)
        return self.success

    # Response

    def conflict(self, message=None):
        return self.status_code(409, message)

    def error(self, message='error'):
        return self.status_code(500, message)

    def unprocessable_entity(self, message=None):
        return self.status_code(422, message)


class FormBinder(object):
    def __init__(self, **kwargs):
        annotations = self.__annotations__
        data = dict_key_camel_to_snake(kwargs)

        for k, v in data.items():
            if k not in annotations:
                continue

            self.__dict__[k] = v


def get_data_range(rq: Request):
    limit = int(rq.query.get('limit', [10])[0])
    page = int(rq.query.get('page', [1])[0])
    return limit * (page - 1), limit


async def send_file(value: bytes | Path | str, content_type: Optional[str] = 'application/octet-stream'):
    if isinstance(value, Path):
        value = str(value)

    if not (is_bytes := isbytes(value)) and not isfile(value):
        return not_found()

    if content_type is None:
        file_data = value if is_bytes else await aread_file(value)
        content_type = '/'.join(get_file_mime(file_data))

    try:
        return file(value, content_type)
    except:
        return not_found()


async def send_ico(value: bytes | Path | str):
    return await send_file(value, 'image/x-icon')


async def send_pil_image(image: Image):
    image_file = save_file_as_bytesio(image.save, True, format='webp')
    return await send_webp(image_file)


async def send_webp(value: bytes | Path | str):
    return await send_file(value, 'image/webp')
