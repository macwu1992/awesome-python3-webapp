import orm
import models

def test():
   yield from orm.create_pool(user='test', password='test')
   users = models.User(email='test@test.com', passwd='test', image='about:blank')

   yield from users.save()

   for x in test():
       pass