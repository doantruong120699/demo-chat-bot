from pscds.models import User, Log, TaskUser, TimeInterval, ProjectUser
from langchain_core.tools import StructuredTool, Tool
from agents.services.io_models.input import UserIdInput, EmailInput

class PSCDUsersService:
    def _mapping_role_id_to_name(self, role_id: int) -> str:
        """Mapping role ID to role name"""
        if role_id == 1:
            return "Admin"
        elif role_id == 2:
            return "Manager"
        elif role_id == 3:
            return "User"
        else:
            return "Unknown"
    # User-related methods
    def _get_user_info_by_email(self, email: str) -> str:
        """Get user information by email address"""
        try:
            user = User.objects.get(email=email)
            return f"User Info - Full name: {user.full_name}, Email: {user.email}, Role ID: {self._mapping_role_id_to_name(user.role_id)}, Phone: {user.phone}, Address: {user.address}, Date of birth: {user.datebirth}, Active: {user.active}, Created at: {user.created_at}"
        except User.DoesNotExist:
            return "User not found"

    def _get_user_info_by_id(self, user_id: int) -> str:
        """Get user information by user ID"""
        try:
            user = User.objects.get(id=user_id)
            return f"User Info - ID: {user.id}, Full name: {user.full_name}, Email: {user.email}, Role ID: {self._mapping_role_id_to_name(user.role_id)}, Phone: {user.phone}, Address: {user.address}, Active: {user.active}"
        except User.DoesNotExist:
            return "User not found"

    def _get_all_users(self) -> str:
        """Get list of all users"""
        users = User.objects.all()
        if not users:
            return "No users found"
        
        result = "All Users:\n"
        for user in users:
            result += f"- ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Role: {self._mapping_role_id_to_name(user.role_id)}, Active: {user.active}\n"
        return result

    def _count_users(self) -> str:
        """Count total number of users"""
        count = User.objects.count()
        return f"Total number of users: {count}"

    def _get_recent_logs_by_user(self, user_id: int, limit: int = 10) -> str:
        """Get recent activity logs for a specific user"""
        try:
            logs = Log.objects.filter(user_id=user_id).order_by('-time')[:limit]
            if not logs:
                return f"No logs found for user ID: {user_id}"
            
            result = f"Recent {limit} logs for User ID {user_id}:\n"
            for log in logs:
                result += f"- Time: {log.time}, Event: {log.event}, Situation: {log.sit}, Location: {log.location}, OS: {log.os}\n"
            return result
        except Exception as e:
            return f"Error retrieving logs: {str(e)}"
        
    def _get_user_statistics(self, user_id: int) -> str:
        """Get statistics for a specific user"""
        try:
            user = User.objects.get(id=user_id)
            task_users = TaskUser.objects.filter(user_id=user_id)
            total_tasks = task_users.count()
            
            completed_tasks = sum(1 for tu in task_users if tu.task.status_id == 3)
            total_work_time = sum(tu.task.work_time for tu in task_users)
            
            time_intervals = TimeInterval.objects.filter(user_id=user_id)
            total_intervals = time_intervals.count()
            
            projects = ProjectUser.objects.filter(user_id=user_id).count()
            
            completion_rate = (completed_tasks/total_tasks*100) if total_tasks > 0 else 0
            return f"User Statistics for '{user.full_name}':\n- Assigned Tasks: {total_tasks}\n- Completed Tasks: {completed_tasks}\n- Total Work Time: {total_work_time}h\n- Time Intervals: {total_intervals}\n- Active Projects: {projects}\n- Task Completion Rate: {completion_rate:.1f}%"
        except User.DoesNotExist:
            return "User not found"
        except Exception as e:
            return f"Error calculating user statistics: {str(e)}"
        
    def create_tools(self):
        return [
            StructuredTool.from_function(
                func=self._get_user_info_by_email,
                name="get_user_info_by_email",
                description="Get detailed user information by email address",
                args_schema=EmailInput
            ),
            StructuredTool.from_function(
                func=self._get_user_info_by_id,
                name="get_user_info_by_id", 
                description="Get detailed user information by user ID",
                args_schema=UserIdInput
            ),
            Tool(
                name="get_all_users",
                func=lambda *args, **kwargs: self._get_all_users(),
                description="Get list of all users in the system. No input required."
            ),
            Tool(
                name="count_users",
                func=lambda *args, **kwargs: self._count_users(),
                description="Count total number of users in the system. No input required."
            ),
            StructuredTool.from_function(   
                func=self._get_recent_logs_by_user,
                name="get_recent_logs_by_user",
                description="Get recent activity logs for a specific user",
                args_schema=UserIdInput
            ),
            StructuredTool.from_function(
                func=self._get_user_statistics,
                name="get_user_statistics",
                description="Get statistics for a specific user",
                args_schema=UserIdInput
            ),
        ]