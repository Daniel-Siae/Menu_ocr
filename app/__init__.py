from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # 允许跨域请求
    
    # 加载配置
    app.config.from_object('config.Config')
    
    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)
    
    return app