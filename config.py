import os
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载 .env 文件
load_dotenv()

class Config:
    # API密钥配置
    GLM_4_1V_API_KEY = os.getenv('GLM_4_1V_API_KEY')
    GLM_4_5_AIR_API_KEY = os.getenv('GLM_4_5_AIR_API_KEY')
    
    # API基础URL
    API_BASE_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
    
    # 验证配置
    @classmethod
    def validate(cls):
        if not cls.GLM_4_1V_API_KEY:
            logger.warning("GLM_4_1V_API_KEY not found in environment variables")
        if not cls.GLM_4_5_AIR_API_KEY:
            logger.warning("GLM_4_5_AIR_API_KEY not found in environment variables")

# 在应用启动时验证配置
Config.validate()