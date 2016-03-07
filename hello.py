import orm, asyncio
from models import User, Blog

def test(loop):
   yield from orm.create_pool(loop=loop, user='root', password='', db='awesome')
   users = User(name='Test1', email='test@example.com1', passwd='12345678901', image='about:blank1')
   blog = Blog(user_id = '123')

   yield from users.save()
   yield from blog.save()

loop = asyncio.get_event_loop()
test(loop)
loop.close()