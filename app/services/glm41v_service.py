import requests
import json
import logging
from config import Config

# 配置日志
logger = logging.getLogger(__name__)

class GLM41VService:
    def __init__(self):
        self.api_key = Config.GLM_4_1V_API_KEY
        self.base_url = Config.API_BASE_URL
        
        # 验证API密钥
        if not self.api_key:
            raise ValueError("GLM_4_1V_API_KEY is not set in the configuration")

    def recognize_menu(self, image_base64):
        url = self.base_url
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "glm-4v-flash",
            "temperature": 0.9,
            "top_k": 4,
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": '''请识别这张图片中的菜单内容，提取所有菜品的名称、描述和价格，并以结构化的JSON格式返回。请按照菜品类别组织菜品，每个类别作为一个键，值为该类别下的菜品列表。每道菜必须包含'name'（名称）、'description'（描述）和'price'（价格）字段。描述应该详细且有吸引力，可以从菜品的口味、制作方式、主要食材等方面进行描述。

例如：
```json
{
  "type1：冷菜": [
    {"name": "拍黄瓜", "description": "清爽开胃，夏日解暑佳品", "price": 12.0},
    {"name": "凉拌木耳", "description": "营养丰富，搭配香菜和小米辣，口感爽脆", "price": 15.0}
  ],
  "type2：热菜": [
    {"name": "宫保鸡丁", "description": "经典川菜，酸甜微辣，色香味俱全", "price": 38.0},
    {"name": "鱼香肉丝", "description": "酸甜可口，口感层次丰富", "price": 32.0}
  ]
}
```

重要提示：
1. 请严格按照上述格式输出，使用```json和```包围JSON内容
2. 每道菜必须包含'name'、'description'、'price'三个字段
3. 'price'字段必须是数字类型（如12.0），不要包含货币符号或其他文字
4. 'description'字段不超过8个字。
5. 请只返回JSON代码块，不要添加其他解释文字'''
                        }
                    ]
                }
            ]
        }
        
        try:
            logger.info("Calling GLM-4.1V API for menu recognition")
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            logger.info("Successfully received response from GLM-4.1V API")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"GLM-4.1V API call failed: {str(e)}")
            raise Exception(f"GLM-4.1V API 调用失败: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GLM-4.1V API response: {str(e)}")
            raise Exception(f"解析 GLM-4.1V API 响应失败: {str(e)}")