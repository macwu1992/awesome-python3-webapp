# # 最基本的url处理
# from aiohttp import web
# import asyncio
#
# @asyncio.coroutine
# def handler1(request):
#     return web.Response(body=b'this is handler 1')
#
# def handler2(request):
#     return web.Response(body=b'this is handler 2')
#
# app1 = web.Application()
#
# app2 = web.Application()
#
# app1.router.add_route('GET', '/handler1', handler1)
# app2.router.add_route('GET', '/handler2', handler2)
#
# web.run_app(app1)
# web.run_app(app2)

path = 'a.sdaf'
print(path[path.find('.'):])
