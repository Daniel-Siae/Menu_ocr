import requests
import json
from config import Config

class GLM45AirService:
    def __init__(self):
        self.api_key = Config.GLM_4_5_AIR_API_KEY
        self.base_url = Config.API_BASE_URL

    def analyze_health(self, dish_list):
        url = self.base_url
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 检查菜品列表是否为空
        if not dish_list:
            # 如果菜品列表为空，返回空的响应结构
            return {
                "choices": [{
                    "message": {
                        "content": "```json\n[]\n```"
                    }
                }]
            }
        
        # 构造菜品列表字符串
        dish_list_str = ""
        for dish in dish_list:
            dish_list_str += f"{dish['name']}: {dish['description']}\n"
        
        payload = {
            "model": "glm-4-flash",
            "temperature": 0.9,
            "top_k": 4,
            "max_tokens": 8192,  # 减少max_tokens以控制输出长度
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的营养师，能够分析菜品的营养成分。"
                },
                {
                    "role": "user",
                    "content": f"请分析以下菜品的营养成分:\\n{dish_list_str}\\n请为每道菜提供估算的卡路里、蛋白质(g)、碳水化合物(g)和脂肪(g)。以JSON数组格式返回，每个对象包含name, calories, protein, carbs, fat字段。不要包含健康评价描述。"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"GLM-4.5-Air API (健康分析) 调用失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析 GLM-4.5-Air API (健康分析) 响应失败: {str(e)}")

    def recommend_dishes(self, dish_list_with_nutrition):
        url = self.base_url
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 检查菜品列表是否为空
        if not dish_list_with_nutrition:
            # 如果菜品列表为空，返回空的推荐列表
            return {
                "choices": [{
                    "message": {
                        "content": "```json\n[]\n```"
                    }
                }]
            }
        
        payload = {
            "model": "glm-4-flash",
            "temperature": 0.9,
            "top_k": 4,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的营养师，能够根据营养成分推荐健康的菜品组合。"
                },
                {
                    "role": "user",
                    "content": f"以下是包含营养信息的菜品列表:\n{json.dumps(dish_list_with_nutrition, ensure_ascii=False, indent=2)}\n\n请根据健康程度（低卡路里、低脂肪、高蛋白等综合因素）对这些菜品进行排序，并推荐最健康的1-3个单品或搭配合理的组合。请以JSON数组格式返回推荐的菜品。"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"GLM-4.5-Air API (推荐) 调用失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析 GLM-4.5-Air API (推荐) 响应失败: {str(e)}")

    def generate_nutrition_summary(self, recommended_dishes):
        url = self.base_url
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 检查推荐菜品列表是否为空
        if not recommended_dishes:
            # 如果推荐菜品列表为空，返回空的营养总结
            return {
                "choices": [{
                    "message": {
                        "content": "```json\n{\n  \"totalCalories\": 0,\n  \"totalProtein\": 0,\n  \"totalCarbs\": 0,\n  \"totalFat\": 0\n}\n```"
                    }
                }]
            }
        
        payload = {
            "model": "glm-4-flash",
            "temperature": 0.9,
            "top_k": 4,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的营养师，能够总结菜品的综合营养信息。"
                },
                {
                    "role": "user",
                    "content": f"以下是推荐的菜品及其营养信息:\n{json.dumps(recommended_dishes, ensure_ascii=False, indent=2)}\n\n请生成这些菜品的综合营养总结，包括总热量(kcal)、总蛋白质(g)、总碳水化合物(g)和总脂肪(g)。请以JSON对象格式返回，包含totalCalories, totalProtein, totalCarbs, totalFat字段。"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"GLM-4.5-Air API (营养总结) 调用失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析 GLM-4.5-Air API (营养总结) 响应失败: {str(e)}")