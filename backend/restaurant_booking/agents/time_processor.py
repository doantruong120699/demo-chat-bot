import re
from datetime import datetime, timedelta
from typing import Dict, Optional

class VietnameseTimeProcessor:
    """Xử lý các cụm từ thời gian tiếng Việt"""
    
    def __init__(self):
        self.days = {
            'hôm nay': ['hôm nay', 'nay'],
            'hôm qua': ['hôm qua', 'qua'],
            'ngày mai': ['ngày mai', 'mai']
        }
        
        self.weekdays = {
            'thứ 2': 0, 'thứ hai': 0, 'thứ 3': 1, 'thứ ba': 1,
            'thứ 4': 2, 'thứ tư': 2, 'thứ 5': 3, 'thứ năm': 3,
            'thứ 6': 4, 'thứ sáu': 4, 'thứ 7': 5, 'thứ bảy': 5,
            'chủ nhật': 6
        }

    def process_time_expression(self, text: str) -> Dict[str, Optional[str]]:
        """Xử lý biểu thức thời gian và trả về ngày cụ thể"""
        text = text.lower().strip()
        return {
            'booking_date': self._extract_date(text),
            'booking_time': None  # Không xử lý giờ
        }

    def _extract_date(self, text: str) -> Optional[str]:
        """Trích xuất ngày từ văn bản"""
        today = datetime.now()
        
        # Kiểm tra ngày tương đối
        for day_type, keywords in self.days.items():
            if any(keyword in text for keyword in keywords):
                if day_type == 'hôm nay':
                    return today.strftime('%Y-%m-%d')
                elif day_type == 'hôm qua':
                    return (today - timedelta(days=1)).strftime('%Y-%m-%d')
                elif day_type == 'ngày mai':
                    return (today + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Kiểm tra thứ trong tuần
        for weekday_text, weekday_num in self.weekdays.items():
            if weekday_text in text:
                days_ahead = weekday_num - today.weekday()
                if days_ahead < 0:
                    days_ahead += 7
                return (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        return None

    def is_time_expression(self, text: str) -> bool:
        """Kiểm tra xem văn bản có chứa biểu thức thời gian không"""
        text = text.lower().strip()
        
        # Kiểm tra từ khóa ngày
        all_keywords = []
        for keywords in self.days.values():
            all_keywords.extend(keywords)
        all_keywords.extend(self.weekdays.keys())
        
        return any(keyword in text for keyword in all_keywords)

    def enhance_time_understanding(self, text: str) -> str:
        """Cải thiện khả năng hiểu thời gian"""
        if not self.is_time_expression(text):
            return text
            
        processed = self.process_time_expression(text)
        
        if processed['booking_date']:
            today = datetime.now().date()
            date_obj = datetime.strptime(processed['booking_date'], '%Y-%m-%d').date()
            
            if date_obj == today:
                return f"{text} (tức là ngày hôm nay)"
            elif date_obj == today - timedelta(days=1):
                return f"{text} (tức là ngày hôm qua)"
            elif date_obj == today + timedelta(days=1):
                return f"{text} (tức là ngày ngày mai)"
            else:
                return f"{text} (tức là ngày {date_obj.strftime('%d/%m/%Y')})"
        
        return text
