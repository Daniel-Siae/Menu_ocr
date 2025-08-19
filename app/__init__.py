import os
from flask import Flask
from flask_cors import CORS

def create_app():
    # 检测是否在Vercel环境中
    is_vercel = os.getenv('VERCEL') == '1'
    
    app = Flask(__name__)
    
    # 在Vercel环境中配置CORS
    if is_vercel:
        # Vercel环境中更宽松的CORS配置
        CORS(app, origins=["*"], supports_credentials=True)
    else:
        # 本地开发环境的CORS配置
        CORS(app)
    
    # 加载配置
    try:
        app.config.from_object('config.Config')
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
        # 在Vercel环境中设置基本配置
        app.config['GLM_4_1V_API_KEY'] = os.getenv('GLM_4_1V_API_KEY', '')
        app.config['GLM_4_5_AIR_API_KEY'] = os.getenv('GLM_4_5_AIR_API_KEY', '')
        app.config['API_BASE_URL'] = os.getenv('API_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')
    
    # 注册蓝图
    try:
        from app.routes import main
        app.register_blueprint(main)
    except Exception as e:
        print(f"Error registering blueprint: {e}")
    
    # 健康检查路由
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'environment': 'vercel' if is_vercel else 'local'}
    
    return app