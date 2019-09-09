from peewee import *
from playhouse.db_url import connect
from decouple import config


db_proxy = Proxy()
db = connect(config("DATABASE_URL", default='sqlite:///smusxDB.sqlite', cast=str), autorollback=True)
db_proxy.initialize(db)


class Users(Model):                                                                   # username-model for stat-tracking
    uid = BigIntegerField()
    username = CharField()

    class Meta:
        database = db


if not Users.table_exists():                                                         # creating usernames if not present
    db.create_tables([Users])


class Tracks(Model):                                                                     # track-model for stat-tracking
    user = ForeignKeyField(model=Users, backref='tracks')
    title = TextField(null=True)
    performer = TextField(null=True)
    file_id = TextField(null=True)
    download_url = TextField(null=True)

    class Meta:
        database = db


if not Tracks.table_exists():                                                           # creating tracks if not present
    db.create_tables([Tracks])
