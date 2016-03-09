#这是数据库连接测试,成功,可从数据库获取连接,并进行selecet语句的操作

import asyncio
import aiomysql
import orm
from models import User

loop = asyncio.get_event_loop()

@asyncio.coroutine
def run():
    yield from orm.create_pool(host='127.0.0.1', port=3306,
                                           user='root', password='root',
                                           db='awesome', loop=loop)

    users_table = yield from User.findAll()
    print(users_table)
    # print(getattr(run, '__method__'))

loop.run_until_complete(run())