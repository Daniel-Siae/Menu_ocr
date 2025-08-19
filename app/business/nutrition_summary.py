from app.services.glm45_air_service import GLM45AirService

class NutritionSummary:
    def __init__(self, glm45_air_service):
        self.glm45_air_service = glm45_air_service

    def generate(self, recommended_dishes):
        """
        生成营养总结报告
        """
        try:
            # 调用 GLM-4.5-Air API 生成营养总结
            response = self.glm45_air_service.generate_nutrition_summary(recommended_dishes)
            
            # 解析响应并返回营养总结
            # GLM API响应格式: {'choices': [{'message': {'content': '...'}}]}
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0].get('message', {}).get('content', '')
                
                # 提取JSON部分
                import re
                import json
                json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                    summary_data = json.loads(json_content)
                    return summary_data
                else:
                    # 如果没有JSON格式，返回空对象
                    return {}
            return {}
        except Exception as e:
            raise Exception(f"生成营养总结失败: {str(e)}")