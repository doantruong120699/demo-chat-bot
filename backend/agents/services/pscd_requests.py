from pscds.models import Request
from langchain_core.tools import StructuredTool
from agents.services.io_models.input import UserIdInput, DateRangeInput
from datetime import datetime, timedelta

class PSCDRequestsService:
    def _get_requests_by_user(self, user_id: int) -> str:
        """Get all requests by a specific user"""
        try:
            requests = Request.objects.filter(user_id=user_id).order_by('-created_at')
            if not requests:
                return f"No requests found for user ID: {user_id}"
            
            result = f"Requests for User ID {user_id}:\n"
            for req in requests:
                result += f"- ID: {req.id}, Start: {req.datetime_start}, End: {req.datetime_end}, Reason: {req.reason}, Status: {req.status}\n"
            return result
        except Exception as e:
            return f"Error retrieving requests: {str(e)}"
        
    def _get_requests_in_date_range(self, start_date: str, end_date: str) -> str:
        """Get all requests in a specific date range"""
        try:
            requests = Request.objects.filter(
                datetime_start__date__gte=start_date, 
                datetime_start__date__lte=end_date
            ).order_by('-created_at')
            if not requests:
                return f"📅 Không tìm thấy yêu cầu nào trong khoảng thời gian: {start_date} đến {end_date}"

            result = f"📋 **DANH SÁCH YÊU CẦU**\n📅 Thời gian: {start_date} ➡️ {end_date}\n"
            result += "────────────────────────────\n"
            for idx, req in enumerate(requests, 1):
                result += (
                    f"#{idx}. 👤 **Người gửi:** {req.user.full_name}\n"
                    f"   🆔 Mã yêu cầu: {req.id}\n"
                    f"   ⏰ Thời gian: {req.datetime_start.strftime('%Y-%m-%d %H:%M')} ➡️ {req.datetime_end.strftime('%Y-%m-%d %H:%M')}\n"
                    f"   📝 Lý do: {req.reason}\n"
                    f"   📌 Trạng thái: {req.status}\n"
                    "────────────────────────────\n"
                )
            return result.strip()
        except Exception as e:
            return f"❌ Lỗi khi truy xuất yêu cầu: {str(e)}"
        
    def _get_requests_today(self) -> str:
        """Get all requests for today"""
        return self._get_requests_in_date_range(datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
    
    def _get_requests_yesterday(self) -> str:
        """Get all requests for yesterday"""
        return self._get_requests_in_date_range((datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
    
    def _get_requests_tomorrow(self) -> str:
        """Get all requests for tomorrow"""
        return self._get_requests_in_date_range(datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
    
    def _get_requests_this_week(self) -> str:
        """Get all requests for this week"""
        return self._get_requests_in_date_range(datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
    
    def _get_requests_last_week(self) -> str:
        """Get all requests for last week"""
        return self._get_requests_in_date_range((datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
    
    def _get_requests_next_week(self) -> str:
        """Get all requests for next week"""
        return self._get_requests_in_date_range((datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        
    def create_tools(self):
        return [
            StructuredTool.from_function(
                func=self._get_requests_by_user,
                name="get_requests_by_user",
                description="Get all requests by a specific user",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._get_requests_in_date_range,
                name="get_requests_in_date_range",
                description="Get all requests in a specific date range. Date format: YYYY-MM-DD",
                args_schema=DateRangeInput
            ),
            StructuredTool.from_function(
                func=self._get_requests_today,
                name="get_requests_today",
                description="Get all requests for today",
            ),
            StructuredTool.from_function(
                func=self._get_requests_yesterday,
                name="get_requests_yesterday",
                description="Get all requests for yesterday",
            ),
            StructuredTool.from_function(
                func=self._get_requests_tomorrow,
                name="get_requests_tomorrow",
                description="Get all requests for tomorrow",
            ),
            StructuredTool.from_function(
                func=self._get_requests_this_week,
                name="get_requests_this_week",
                description="Get all requests for this week",
            ),
            StructuredTool.from_function(
                func=self._get_requests_last_week,
                name="get_requests_last_week",
                description="Get all requests for last week",
            ),
            StructuredTool.from_function(
                func=self._get_requests_next_week,
                name="get_requests_next_week",
                description="Get all requests for next week",
            ),
        ]