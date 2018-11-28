from aiohttp import web

import storage

routes = web.RouteTableDef()


@routes.post('/')
async def upload(request):
    data = await request.post()
    try:
        file = data['file'].file
        file_bytes = file.read()
        file_hash = storage.save(file_bytes)
        return web.json_response({'file_hash': file_hash})
    except KeyError:
        raise web.HTTPBadRequest(text="'file' key was not found")


def find_file(action):

    async def wrap(request):
        file_hash = request.match_info['hash']

        if not storage.valid_hash(file_hash):
            raise web.HTTPBadRequest(text='invalid hash parameter')

        try:
            action(file_hash)
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
