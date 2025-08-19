from app import create_app

# 创建应用实例
application = create_app()

# Vercel需要一个app对象作为WSGI应用
app = application

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)