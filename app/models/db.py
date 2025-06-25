from peewee import MySQLDatabase, Model, AutoField

db = MySQLDatabase(
    host='localhost',
    user='cogito_dba',
    password='1234',
    database='cogito_db'
)


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = db
