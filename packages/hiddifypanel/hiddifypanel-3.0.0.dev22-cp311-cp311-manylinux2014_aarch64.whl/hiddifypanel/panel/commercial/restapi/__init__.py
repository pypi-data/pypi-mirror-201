from flask import Blueprint
from flask_restful import Api
from .tgbot import bot,register_bot,TGBotResource


bp = Blueprint("api", __name__, url_prefix="/<proxy_path>/<user_secret>/api/v1")
api = Api(bp)


def init_app(app):   
    api.add_resource(TGBotResource, "/tgbot/")
    with app.app_context():
        register_bot()        
    app.register_blueprint(bp)
#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product
