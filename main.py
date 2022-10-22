import json
from aiohttp import web
from gino import Gino


PG_DSN = 'postgres://aiohttp:1234@127.0.0.1:5431/aiohttpdb'

app = web.Application()
db = Gino()


# class HTTPException(web.HTTPClientError):
#
#     def __init__(self, *args, error='', **kwargs):
#         kwargs['text'] = json.dumps({'error': error})
#         super().__init__(*args, **kwargs, content_type='application/json')
#
#
# class BadRequest(HTTPException):
#     status_code = 400
#
#
# class NotFound(HTTPException):
#     status_code = 404
#

class Ads(db.Model):
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String, nullable=False)
    date_cr = db.Column(db.DateTime, server_default=db.func.now())
    owner = db.Column(db.String, nullable=False)


async def init_orm(app):
    print('START APP')
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('CLOSE APP')


class AdsViev(web.View):

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Ads.get(adv_id)
        if adv is None:
            raise web.HTTPBadRequest(text=json.dumps(
                {
                    'error': 'not found'
                }
            ), content_type='application/json')
        else:
            return web.json_response(
                {
                    'id': adv.id,
                    'title': adv.title,
                    'description': adv.description,
                    'date_cr': str(adv.date_cr),
                    'owner': adv.owner
                }
            )

    async def post(self):
        adv_new = await self.request.json()
        adv = await Ads.create(
                title=adv_new['title'],
                description=adv_new['description'],
                owner=adv_new['owner']
            )

        return web.json_response({'adv_id': adv.id})

    async def put(self):
        adv_new = await self.request.json()
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Ads.get(adv_id)
        if adv is None:
            raise web.HTTPBadRequest(text=json.dumps(
                {
                    'error': 'not found'
                }
            ), content_type='application/json')
        else:
            await adv.update(
                title=adv_new['title'],
                description=adv_new['description']
            ).apply()
            return web.json_response(
                {
                    'id': adv.id,
                    'title': adv.title,
                    'description': adv.description,
                    'date_cr': str(adv.date_cr),
                    'owner': adv.owner
                }
            )

    async def delete(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Ads.get(adv_id)
        if adv is None:
            raise web.HTTPBadRequest(text=json.dumps(
                {
                    'error': 'not found'
                }
            ), content_type='application/json')
        else:
            await adv.delete()
            return web.json_response({'status': 'deleted'})


app.router.add_route('GET', '/ads/{adv_id:\d+}', AdsViev)
app.router.add_route('POST', '/ads/', AdsViev)
app.router.add_route('PUT', '/ads/{adv_id:\d+}', AdsViev)
app.router.add_route('DELETE', '/ads/{adv_id:\d+}', AdsViev)

app.cleanup_ctx.append(init_orm)

web.run_app(app)