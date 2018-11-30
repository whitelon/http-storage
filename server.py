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


def find_file(request, action):
    file_hash = request.match_info['hash']

    if not storage.valid_hash(file_hash):
        raise web.HTTPBadRequest(text='invalid hash parameter')

    try:
        return action(file_hash)
    except FileNotFoundError:
        raise web.HTTPNotFound()


@routes.get('/{hash}')
async def download(request):
    def download_action(file_hash):
        file = storage.get_path(file_hash)
        return web.FileResponse(file)

    return find_file(request, download_action)


@routes.delete('/{hash}')
async def delete(request):
    def delete_action(file_hash):
        storage.delete(file_hash)
        return web.Response(text='File deleted')

    return find_file(request, delete_action)


app = web.Application()
app.add_routes(routes)


def run():
    web.run_app(app, port=44184)


if __name__ == '__main__':
    run()
