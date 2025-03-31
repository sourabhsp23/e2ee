from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=100)

class Message(models.Model):
    id = fields.IntField(pk=True)
    sender = fields.CharField(max_length=50)
    recipient = fields.CharField(max_length=50)
    encrypted_message = fields.TextField()
    encrypted_aes_key = fields.TextField()

def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url="sqlite://database.db",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )
