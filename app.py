#!/Users/Tong/dev_repo/liaoxuefeng_shizhan/awesome-python3-webapp/py34en
# -*- coding: <utf-8> -*-

import logging;
import config
from flask import Flask
from flask import render_template
from models import User
logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

# index 页面，当收到请求时，返回body
# def index(request):
#     return web.Response(body = b'<h1>Awesome Page</h1>')
#
# @asyncio.coroutine
# def init(loop):
# 	app = web.Application(loop = loop)
# 	app.router.add_route('GET', '/', index)
# 	srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
# 	logging.info('Server runing at http://127.0.0.1:9000...')
# 	return srv
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()
# app = Flask(__name__)
# app.config.from_object(config)
#
# @app.route('/', methods=['GET'])
# def index():
# 	users = yield from User.findAll()
# 	return render_template("test.html", users = users)
#
# @app.route("/blog")
# def blog():
# 	return "blog page"
#
# @app.route("/comments")
# def comments():
# 	return "comments page"
#
# print(__name__)
# if __name__ == "__main__":
# 	app.run()
