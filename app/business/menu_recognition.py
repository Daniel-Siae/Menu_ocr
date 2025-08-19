import re
import json

class MenuRecognition:
    def __init__(self, glm41v_service):
        self.glm41v_service = glm41v_service

    def recognize(self, image_base64):
        try:
            # 调用 GLM-4.1V API
            response = self.glm41v_service.recognize_menu(image_base64)
            
            # 解析响应并返回菜单文本
            # GLM API响应格式: {'choices': [{'message': {'content': '...'}}]}
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0].get('message', {}).get('content', '')
                # 提取有效的JSON部分
                return self._extract_valid_json(content)
            return ''
        except Exception as e:
            raise Exception(f"菜单识别失败: {str(e)}")
    
    def _extract_valid_json(self, content):
        """
        从内容中提取有效的JSON部分
        """
        # 查找被```json和```包围的JSON代码块
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', content, re.DOTALL)
        if json_match:
            json_content = json_match.group(1)
            # 验证是否为有效的JSON
            try:
                # 尝试解析JSON以确保其有效性
                json.loads(json_content)
                # 如果解析成功，直接返回JSON内容
                return json_content
            except json.JSONDecodeError:
                # 如果解析失败，尝试清理JSON内容中的异常字符
                cleaned_json = self._clean_json_content(json_content)
                try:
                    json.loads(cleaned_json)
                    return cleaned_json
                except json.JSONDecodeError:
                    # 如果仍然解析失败，返回原始内容让后续处理逻辑处理错误
                    pass
        
        # 如果没有找到有效的JSON代码块，返回原始内容
        return content

    def _clean_json_content(self, json_content):
        """
        清理JSON内容中的异常字符
        """
        # 移除可能导致解析错误的异常字符
        # 移除末尾的多余字符
        cleaned = json_content.strip()
        # 移除可能导致问题的特殊字符
        cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)
        return cleaned