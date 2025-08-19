from app import create_app

# 创建Flask应用实例
app = create_app()

# Vercel需要这个app对象作为WSGI应用入口点
application = app

# 为了本地开发兼容性
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)