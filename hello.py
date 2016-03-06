from orm import Model, StringField, IntegerField

class User(Model):
    __table__ = 'user'

    id = IntegerField(primary_key = True)
    name = StringField

user = User(id=123, name='Michael')
yield from user.save()
