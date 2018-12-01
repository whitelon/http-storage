from datetime import datetime
from hashlib import md5
from pathlib import Path

from aiohttp import web

import storage

routes = web.RouteTableDef()


async def save_file(reader):
    tempfile = Path(f"temp{datetime.now()}")
    md = md5()

    with tempfile.open(mode='wb') as f:
        while True:
            chunk = await reader.read_chunk()
            if not chunk:
                break
            f.write(chunk)
            md.update(chunk)

    file_hash = md.hexdigest()
    file_hash = storage.move(tempfile, file_hash)

    return file_hash


@routes.post('/')
async def upload(request):
    data = await request.multipart()

    async for field in data:
        if field.name == 'file':
            file_hash = await save_file(field)
            return web.json_response({'file_hash': file_hash})

    raise web.HTTPBadRequest(text="'file' key was not found")


def find_file(action):
    async def wrap(request):
        file_hash = request.match_info['hash']

        if not storage.valid_hash(file_hash):
            raise web.HTTPBadRequest(text='invalid hash parameter')

        try:
            return action(file_hash)
        except FileNotFoundError:
            raise web.HTTPNotFound()

    return wrap


@routes.get('/{hash}')
@find_file
def download(file_hash):
    file = storage.get_path(file_hash)
    return web.FileResponse(file)


@routes.delete('/{hash}')
@find_file
def delete(file_hash):
    storage.delete(file_hash)
    return web.Response(text='File deleted')


app = web.Application()
app.add_routes(routes)


def run():
    web.run_app(app, port=44184)


if __name__ == '__main__':
    run()
