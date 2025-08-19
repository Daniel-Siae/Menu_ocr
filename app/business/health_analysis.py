from app.services.glm45_air_service import GLM45AirService
import re
import json

class HealthAnalysis:
    def __init__(self, glm45_air_service):
        self.glm45_air_service = glm45_air_service

    def analyze(self, dish_list):
        """
        分析菜品的营养成分
        """
        try:
            print("开始健康分析，菜品列表：", dish_list)
            
            # 调用 GLM-4.5-Air API 进行健康分析
            response = self.glm45_air_service.analyze_health(dish_list)
            print("API响应：", response)
            
            # 解析响应并返回营养成分数据
            # GLM API响应格式: {'choices': [{'message': {'content': '...'}}]}
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0].get('message', {}).get('content', '')
                print("API返回内容：", content)
                
                # 提取JSON部分
                json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                    print("提取到的JSON内容：", json_content)
                    nutrition_data = json.loads(json_content)
                    print("解析后的营养数据：", nutrition_data)
                    
                    # 将营养信息与原始菜品信息合并
                    for i, dish in enumerate(nutrition_data):
                        if i < len(dish_list):
                            # 保留原始菜品的名称、描述和价格
                            dish['name'] = dish_list[i].get('name', dish.get('name', ''))
                            dish['description'] = dish_list[i].get('description', dish.get('description', ''))
                            dish['price'] = dish_list[i].get('price', dish.get('price', 0))
                            # 保留原始文本（如果存在）
                            if 'originalText' in dish_list[i]:
                                dish['originalText'] = dish_list[i]['originalText']
                            # 移除可能存在的健康描述字段
                            dish.pop('healthDescription', None)
                    
                    print("最终返回的营养数据：", nutrition_data)
                    return nutrition_data
                else:
                    print("未找到JSON格式数据，返回原始菜品列表")
                    # 如果没有JSON格式，返回原始菜品列表（没有营养信息）
                    return dish_list
            print("API响应格式不正确，返回空列表")
            return []
        except Exception as e:
            print("健康分析出错：", str(e))
            raise Exception(f"健康分析失败: {str(e)}")