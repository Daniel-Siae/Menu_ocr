from flask import Blueprint, request, jsonify, send_from_directory
import base64
import os
import json
import re
from app.services.glm41v_service import GLM41VService
from app.services.glm45_air_service import GLM45AirService
from app.business.menu_recognition import MenuRecognition
from app.business.cost_calculator import CostCalculator
from app.business.health_analysis import HealthAnalysis
from app.business.recommendation_engine import RecommendationEngine
from app.business.nutrition_summary import NutritionSummary

main = Blueprint('main', __name__, static_folder='static')

# 初始化服务
glm41v_service = GLM41VService()
glm45_air_service = GLM45AirService()
menu_recognition = MenuRecognition(glm41v_service)
cost_calculator = CostCalculator()
health_analysis = HealthAnalysis(glm45_air_service)
recommendation_engine = RecommendationEngine(glm45_air_service)
nutrition_summary = NutritionSummary(glm45_air_service)

@main.route('/')
def index():
    return send_from_directory(os.path.join(main.root_path, '..'), 'index.html')

@main.route('/api/process-menu', methods=['POST'])
def process_menu():
    try:
        # 获取上传的图片
        if 'image' not in request.files:
            return jsonify({'error': '没有找到图片文件'}), 400
        
        image_file = request.files['image']
        
        # 将图片转换为base64
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 1. 菜单识别
        menu_text = menu_recognition.recognize(image_base64)
        print("菜单识别结果：", menu_text)
        
        # 2. 解析菜单文本为菜品列表
        dish_list = parse_menu_text(menu_text)
        print("解析后的菜品列表：", dish_list)
        
        # 3. 健康分析（分析菜品营养成分）
        dish_list_with_nutrition = health_analysis.analyze(dish_list)
        print("健康分析结果：", dish_list_with_nutrition)
        
        # 4. 菜品推荐（根据健康程度推荐菜品）
        recommended_dishes = recommendation_engine.recommend(dish_list_with_nutrition)
        print("推荐菜品结果：", recommended_dishes)
        
        # 5. 生成营养总结
        nutrition_summary_data = nutrition_summary.generate(recommended_dishes)
        print("营养总结结果：", nutrition_summary_data)
        
        # 6. 计算总价
        total_cost = cost_calculator.calculate(recommended_dishes)
        print("总价计算结果：", total_cost)
        
        # 返回结果
        return jsonify({
            'menuText': menu_text,
            'dishList': dish_list_with_nutrition,
            'recommendedDishes': recommended_dishes,
            'nutritionSummary': nutrition_summary_data,
            'totalCost': total_cost
        })
    except Exception as e:
        print("处理菜单时出错：", str(e))
        return jsonify({'error': str(e)}), 500
def parse_menu_text(menu_text):
    """
    解析菜单文本为菜品列表
    支持处理结构化的JSON格式菜单数据和文本格式
    """
    
    # 检查是否包含JSON代码块
    if '```json' in menu_text:
        print("检测到JSON代码块")
        try:
            # 提取JSON部分
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', menu_text, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
                print("提取到代码块中的JSON内容")
                print("JSON内容长度:", len(json_content))
                print("JSON内容预览:", repr(json_content[:100]))
                
                # 清理JSON内容，移除可能的注释和多余空格
                json_content = json_content.strip()
                print("清理前的JSON内容:", repr(json_content[:100]))
                
                # 尝试解析JSON
                menu_data = json.loads(json_content)
                print("JSON解析成功")
                
                # 解析结构化的菜单数据（通用方法）
                dishes = []
                
                # 遍历所有键值对
                if isinstance(menu_data, dict):
                    for key, value in menu_data.items():
                        print(f"处理分类: {key}")
                        # 如果值是列表，且列表中的元素是字典
                        if isinstance(value, list):
                            print(f"  分类 {key} 包含 {len(value)} 个项目")
                            for i, item in enumerate(value):
                                if isinstance(item, dict):
                                    print(f"    处理项目 {i}: {item}")
                                    # 尝试提取菜品信息
                                    # 查找名称键
                                    name = ""
                                    for k in ['name',]:
                                        if k in item:
                                            name = str(item[k])
                                            break
                                    
                                    # 查找描述键
                                    description = ""
                                    for k in ['description']:
                                        if k in item:
                                            description = str(item[k])
                                            break
                                    
                                    # 查找价格键
                                    price = 0
                                    for k in ['price','价格']:
                                        if k in item:
                                            try:
                                                price = float(item[k])
                                            except (ValueError, TypeError):
                                                pass
                                            break
                                    
                                    dish = {
                                        'name': name,
                                        'description': description,
                                        'price': price
                                    }
                                    
                                    # 只有当名称不为空时才添加
                                    if dish['name']:
                                        dishes.append(dish)
                                        print(f"    添加菜品: {dish['name']}")
                
                    # 如果成功解析到菜品，返回结果
                    if dishes:
                        print(f"总共解析到 {len(dishes)} 道菜")
                        return dishes
                    else:
                        print("没有解析到任何菜品")
                else:
                    print("JSON数据不是字典格式")
            else:
                print("未找到有效的JSON代码块")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            print("错误位置附近的内容:", repr(menu_text[max(0, e.pos-50):e.pos+50]))
        except Exception as e:
            print(f"解析过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        # 如果没有代码块，尝试直接解析整个内容为JSON
        print("尝试直接解析菜单文本为JSON")
        try:
            menu_data = json.loads(menu_text)
            print("直接JSON解析成功")
            
            # 解析结构化的菜单数据（通用方法）
            dishes = []
            
            # 遍历所有键值对
            if isinstance(menu_data, dict):
                for key, value in menu_data.items():
                    print(f"处理分类: {key}")
                    # 如果值是列表，且列表中的元素是字典
                    if isinstance(value, list):
                        print(f"  分类 {key} 包含 {len(value)} 个项目")
                        for i, item in enumerate(value):
                            if isinstance(item, dict):
                                print(f"    处理项目 {i}: {item}")
                                # 尝试提取菜品信息
                                # 查找名称键
                                name = ""
                                for k in ['name',]:
                                    if k in item:
                                        name = str(item[k])
                                        break
                                
                                # 查找描述键
                                description = ""
                                for k in ['description']:
                                    if k in item:
                                        description = str(item[k])
                                        break
                                
                                # 查找价格键
                                price = 0
                                for k in ['price','价格']:
                                    if k in item:
                                        try:
                                            price = float(item[k])
                                        except (ValueError, TypeError):
                                            pass
                                        break
                                
                                dish = {
                                    'name': name,
                                    'description': description,
                                    'price': price
                                }
                                
                                # 只有当名称不为空时才添加
                                if dish['name']:
                                    dishes.append(dish)
                                    print(f"    添加菜品: {dish['name']}")
            
                # 如果成功解析到菜品，返回结果
                if dishes:
                    print(f"总共解析到 {len(dishes)} 道菜")
                    return dishes
                else:
                    print("没有解析到任何菜品")
            else:
                print("JSON数据不是字典格式")
        except json.JSONDecodeError as e:
            print(f"直接JSON解析失败: {e}")
        except Exception as e:
            print(f"直接解析过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
    
    # 如果没有找到有效的JSON或解析失败，返回空列表
    print("返回空的菜品列表")
    return []
    

    