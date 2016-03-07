import orm, asyncio
from models import User

def test(loop):
   yield from orm.create_pool(loop=loop, user='root', password='', db='awesome')
   users = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

   yield from users.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()