from aiohttp import web
from datetime import datetime
from pathlib import Path
from hashlib import md5
import storage

routes = web.RouteTableDef()


@routes.post('/')
async def upload(request):
    data = await request.multipart()

    async for field in data:
        if field.name == 'file':
            tempfile = Path(f"temp{datetime.now()}")
            md = md5()

            with tempfile.open(mode='wb') as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
                    md.update(chunk)

            file_hash = md.hexdigest()
            file_hash = storage.move(tempfile, file_hash)

            return web.json_response({'file_hash': file_hash})

    raise web.HTTPBadRequest(text="'file' key was not found")


@routes.get('/{hash}')
async def download(request):
    file_hash = request.match_info['hash']

    if not storage.valid_hash(file_hash):
        raise web.HTTPBadRequest(text='invalid hash parameter')

    try:
        file = storage.get_path(file_hash)
        return web.FileResponse(file)
    except FileNotFoundError:
        raise web.HTTPNotFound()


@routes.delete('/{hash}')
async def delete(request):
    file_hash = request.match_info['hash']

    if not storage.valid_hash(file_hash):
        raise web.HTTPBadRequest(text='invalid hash parameter')

    try:
        storage.delete(file_hash)
        return web.Response(text='File deleted')
    except FileNotFoundError:
        raise web.HTTPNotFound()


app = web.Application()
app.add_routes(routes)


def run():
    web.run_app(app, port=44184)


if __name__ == '__main__':
    run()
