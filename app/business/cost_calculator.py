import math

class CostCalculator:
    def calculate(self, recommended_dishes):
        """
        计算推荐菜品的总价
        """
        try:
            # 确保recommended_dishes是一个列表
            if not isinstance(recommended_dishes, list):
                # 如果不是列表，尝试获取列表
                if hasattr(recommended_dishes, 'items'):
                    # 可能是字典，尝试获取items键
                    if 'items' in recommended_dishes:
                        recommended_dishes = recommended_dishes['items']
                    else:
                        # 如果没有items键，直接使用recommended_dishes
                        recommended_dishes = [recommended_dishes]
                else:
                    # 其他情况，包装成列表
                    recommended_dishes = [recommended_dishes]
            
            # 计算总价
            total = 0
            for dish in recommended_dishes:
                if isinstance(dish, dict):
                    total += dish.get('price', 0)
                # 如果dish不是字典，跳过它
            
            # 使用math库的ceil函数向上取整到分
            return math.ceil(total * 100) / 100
        except Exception as e:
            print(f"费用计算失败: {str(e)}")
            # 出错时返回0而不是抛出异常
            return 0