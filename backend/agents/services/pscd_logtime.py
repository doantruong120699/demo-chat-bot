from pscds.models import User, Log, TaskUser, TimeInterval, ProjectUser
from langchain_core.tools import StructuredTool, Tool
from agents.services.io_models.input import UserIdInput, EmailInput, DateRangeInputByUser
from django.db.models import Sum, Count, F, ExpressionWrapper, DurationField
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.functions import Extract


class PSCDLogTimeService:
    def _statistics_logtime_by_user_in_date_range(self, user_id: int, start_date: str, end_date: str) -> str:
        """Statistics logtime by user ID in date range"""
        try:
            # Convert string dates to datetime objects
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Filter time intervals
            logtime_queryset = TimeInterval.objects.filter(
                user_id=user_id, 
                start_at__date__gte=start_datetime, 
                end_at__date__lte=end_datetime
            ).order_by('start_at')
            
            if not logtime_queryset.exists():
                return f"No logtime data found for user {user_id} from {start_date} to {end_date}"
            
            # Calculate total time by summing individual durations
            total_seconds = 0
            total_activity_fill = 0
            total_mouse_fill = 0
            total_keyboard_fill = 0
            total_jobs = 0
            
            for interval in logtime_queryset:
                # Calculate duration in seconds
                duration = interval.end_at - interval.start_at
                total_seconds += duration.total_seconds()
                
                # Sum other metrics
                total_activity_fill += interval.activity_fill or 0
                total_mouse_fill += interval.mouse_fill or 0
                total_keyboard_fill += interval.keyboard_fill or 0
                if interval.job:
                    total_jobs += 1
            
            # Convert total seconds to hours and minutes
            total_hours = int(total_seconds // 3600)
            total_minutes = int((total_seconds % 3600) // 60)
            
            # Calculate averages
            interval_count = logtime_queryset.count()
            avg_activity_fill = total_activity_fill / interval_count if interval_count > 0 else 0
            avg_mouse_fill = total_mouse_fill / interval_count if interval_count > 0 else 0
            avg_keyboard_fill = total_keyboard_fill / interval_count if interval_count > 0 else 0
            
            result = f"""
📊 THỐNG KÊ THỜI GIAN LÀM VIỆC - User ID: {user_id}
📅 Khoảng thời gian: {start_date} đến {end_date}

⏱️ TỔNG THỜI GIAN: {total_hours} giờ {total_minutes} phút
📈 HOẠT ĐỘNG TRUNG BÌNH:
   • Activity Fill: {avg_activity_fill:.1f}%
   • Mouse Fill: {avg_mouse_fill:.1f}%
   • Keyboard Fill: {avg_keyboard_fill:.1f}%

📋 CHI TIẾT:
   • Số lần ghi nhận: {interval_count}
   • Tổng Activity Fill: {total_activity_fill}%
   • Tổng Mouse Fill: {total_mouse_fill}%
   • Tổng Keyboard Fill: {total_keyboard_fill}%
   • Số công việc: {total_jobs}
            """
            
            return result.strip()
            
        except Exception as e:
            return f"Lỗi khi tính toán thống kê: {str(e)}"

    def _statistics_logtime_by_user_today(self, user_id: int) -> str:
        """Statistics logtime by user ID today"""
        today = timezone.now().date().strftime('%Y-%m-%d')
        return self._statistics_logtime_by_user_in_date_range(user_id, today, today)
    
    def _statistics_logtime_by_user_this_week(self, user_id: int) -> str:
        """Statistics logtime by user ID this week"""
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        return self._statistics_logtime_by_user_in_date_range(
            user_id, 
            start_of_week.strftime('%Y-%m-%d'), 
            end_of_week.strftime('%Y-%m-%d')
        )

    def _statistics_logtime_by_user_this_month(self, user_id: int) -> str:
        """Statistics logtime by user ID this month"""
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        # Get last day of month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        return self._statistics_logtime_by_user_in_date_range(
            user_id, 
            start_of_month.strftime('%Y-%m-%d'), 
            end_of_month.strftime('%Y-%m-%d')
        )

    def _statistics_logtime_by_user_yesterday(self, user_id: int) -> str:
        """Statistics logtime by user ID yesterday"""
        yesterday = (timezone.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
        return self._statistics_logtime_by_user_in_date_range(user_id, yesterday, yesterday)
    
    def _statistics_logtime_by_user_last_week(self, user_id: int) -> str:
        """Statistics logtime by user ID last week"""
        today = timezone.now().date()
        start_of_last_week = today - timedelta(days=today.weekday() + 7)
        end_of_last_week = start_of_last_week + timedelta(days=6)
        
        return self._statistics_logtime_by_user_in_date_range(
            user_id, 
            start_of_last_week.strftime('%Y-%m-%d'), 
            end_of_last_week.strftime('%Y-%m-%d')
        )

    def _statistics_logtime_by_user_last_month(self, user_id: int) -> str:
        """Statistics logtime by user ID last month"""
        today = timezone.now().date()
        
        # Get first day of last month
        if today.month == 1:
            start_of_last_month = today.replace(year=today.year - 1, month=12, day=1)
        else:
            start_of_last_month = today.replace(month=today.month - 1, day=1)
        
        # Get last day of last month
        start_of_this_month = today.replace(day=1)
        end_of_last_month = start_of_this_month - timedelta(days=1)
        
        return self._statistics_logtime_by_user_in_date_range(
            user_id, 
            start_of_last_month.strftime('%Y-%m-%d'), 
            end_of_last_month.strftime('%Y-%m-%d')
        )

    def create_tools(self):
        return [
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_in_date_range,
                name="statistics_logtime_by_user_in_date_range",
                description="Statistics logtime by user ID in date range. Input: user_id, start_date (YYYY-MM-DD), end_date (YYYY-MM-DD)",
                args_schema=DateRangeInputByUser
            ),
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_today,
                name="statistics_logtime_by_user_today",
                description="Statistics logtime by user ID today",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_this_week,
                name="statistics_logtime_by_user_this_week",
                description="Statistics logtime by user ID this week",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_this_month,
                name="statistics_logtime_by_user_this_month",
                description="Statistics logtime by user ID this month",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_yesterday,
                name="statistics_logtime_by_user_yesterday",
                description="Statistics logtime by user ID yesterday",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_last_week,
                name="statistics_logtime_by_user_last_week",
                description="Statistics logtime by user ID last week",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._statistics_logtime_by_user_last_month,
                name="statistics_logtime_by_user_last_month",
                description="Statistics logtime by user ID last month",
                args_schema=UserIdInput
            ),
        ]