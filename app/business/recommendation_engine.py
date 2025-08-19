import math
import json
import re

class RecommendationEngine:
    def __init__(self, glm45_air_service):
        self.glm45_air_service = glm45_air_service

    def recommend(self, dish_list_with_nutrition):
        """
        根据菜品营养信息推荐健康菜品
        """
        try:
            print("开始菜品推荐，菜品列表：", dish_list_with_nutrition)
            
            # 检查菜品列表是否包含营养信息
            has_nutrition_info = self._has_nutrition_info(dish_list_with_nutrition)
            print("菜品列表是否包含营养信息：", has_nutrition_info)
            
            if has_nutrition_info:
                # 如果包含营养信息，则调用 GLM-4.5-Air API 进行菜品推荐
                response = self.glm45_air_service.recommend_dishes(dish_list_with_nutrition)
                print("API响应：", response)
                
                # 解析响应并返回推荐菜品
                # GLM API响应格式: {'choices': [{'message': {'content': '...'}}]}
                if 'choices' in response and len(response['choices']) > 0:
                    content = response['choices'][0].get('message', {}).get('content', '')
                    print("API返回内容：", content)
                    
                    # 提取JSON部分
                    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content, re.DOTALL)
                    if json_match:
                        json_content = json_match.group(1)
                        print("提取到的JSON内容：", json_content)
                        recommended_dishes = json.loads(json_content)
                        print("解析后的推荐菜品：", recommended_dishes)
                        
                        # 对推荐菜品进行后续计算处理
                        processed_dishes = self._process_recommendations(recommended_dishes)
                        print("处理后的推荐菜品：", processed_dishes)
                        
                        return processed_dishes
                    else:
                        print("未找到JSON格式数据，返回空列表")
                        return []
                print("API响应格式不正确，返回空列表")
                return []
            else:
                # 如果不包含营养信息，则直接返回原始菜品列表（不进行推荐）
                # 这种情况下，我们假设所有菜品都是可选的
                print("菜品列表不包含营养信息，直接返回原始菜品列表")
                processed_dishes = self._process_recommendations(dish_list_with_nutrition)
                return processed_dishes
        except Exception as e:
            print("菜品推荐出错：", str(e))
            raise Exception(f"菜品推荐失败: {str(e)}")

    def _has_nutrition_info(self, dish_list):
        """
        检查菜品列表是否包含营养信息
        """
        if not isinstance(dish_list, list) or len(dish_list) == 0:
            return False
            
        # 检查第一个菜品是否包含营养信息字段
        first_dish = dish_list[0]
        if isinstance(first_dish, dict):
            nutrition_fields = ['calories', 'protein', 'carbs', 'fat']
            return any(field in first_dish for field in nutrition_fields)
        
        return False

    def _process_recommendations(self, recommended_dishes):
        """
        对推荐菜品进行后续计算处理
        """
        if not isinstance(recommended_dishes, list):
            return recommended_dishes
            
        processed_dishes = []
        for dish in recommended_dishes:
            if isinstance(dish, dict):
                # 创建菜品副本以避免修改原始数据
                processed_dish = dish.copy()
                
                # 获取营养信息（如果存在）
                calories = dish.get('calories', 0)
                protein = dish.get('protein', 0)
                carbs = dish.get('carbs', 0)
                fat = dish.get('fat', 0)
                price = dish.get('price', 0)
                
                # 使用math库进行一些计算
                # 计算营养密度（蛋白质/卡路里比率）
                if calories > 0:
                    protein_density = math.ceil((protein / calories) * 1000) / 1000
                    processed_dish['proteinDensity'] = protein_density
                else:
                    processed_dish['proteinDensity'] = 0
                
                # 计算性价比（蛋白质/价格比率）
                if price > 0:
                    protein_value = math.ceil((protein / price) * 100) / 100
                    processed_dish['proteinValue'] = protein_value
                else:
                    processed_dish['proteinValue'] = 0
                
                # 计算健康评分（综合考虑卡路里、脂肪和蛋白质）
                health_score = 0
                if calories > 0:
                    # 低卡路里得分（卡路里越低得分越高）
                    calorie_score = math.ceil((1 - min(calories / 1000, 1)) * 100) / 100
                    
                    # 低脂肪得分（脂肪越低得分越高）
                    fat_score = math.ceil((1 - min(fat / 50, 1)) * 100) / 100
                    
                    # 高蛋白得分（蛋白质越高得分越高）
                    protein_score = math.ceil(min(protein / 50, 1) * 100) / 100
                    
                    # 综合评分（加权平均）
                    health_score = math.ceil((calorie_score * 0.4 + fat_score * 0.3 + protein_score * 0.3) * 100) / 100
                
                processed_dish['healthScore'] = health_score
                
                processed_dishes.append(processed_dish)
            else:
                processed_dishes.append(dish)
        
        return processed_dishes