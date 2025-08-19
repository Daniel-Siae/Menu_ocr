from app import create_app

# 创建Flask应用实例
app = create_app()

# Vercel需要这个app对象作为WSGI应用入口点
application = app

def handler(event, context):
    """
    Vercel serverless function handler
    """
    # 导入Vercel的WSGI适配器
    from werkzeug.wrappers import Request, Response
    from werkzeug.serving import run_simple
    
    # 将Vercel事件转换为WSGI environ
    with app.request_context(event.get('path', '/'), 
                            method=event.get('httpMethod', 'GET'),
                            headers=event.get('headers', {})):
        try:
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Internal Server Error: {str(e)}'
            }

# 为了本地开发兼容性
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)