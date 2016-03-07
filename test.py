import asyncio
import aiomysql
import orm
from models import User

loop = asyncio.get_event_loop()

@asyncio.coroutine
def go():
    pool = yield from orm.create_pool(host='127.0.0.1', port=3306,
                                           user='root', password='root',
                                           db='awesome', loop=loop)

    users = User(name='Test', email='test@example.com1', passwd='12345678901', image='about:blank1')
    yield from users.save()

    yield from pool.wait_closed()

loop.run_until_complete(go())