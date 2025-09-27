from pscds.models import Project, Task, TaskUser, ProjectUser
from langchain_core.tools import StructuredTool, Tool
from agents.services.io_models.input import ProjectIdInput, UserIdInput, TaskIdInput

class PSCDProjectsService:
    # Project-related methods
    def _mapping_role_id_to_name(self, role_id: int) -> str:
        """Mapping role ID to role name"""
        if role_id == 1:
            return "Project Manager"
        elif role_id == 2:
            return "Leader"
        elif role_id == 3:
            return "Developer"
        elif role_id == 4:
            return "Tester"
        elif role_id == 5:
            return "Designer"
        elif role_id == 6:
            return "Tester"
        else:
            return "Unknown"
        
    def _get_project_info_by_id(self, project_id: int) -> str:
        """Get project information by project ID"""
        try:
            project = Project.objects.get(id=project_id)
            result = (
                f"📁 **THÔNG TIN DỰ ÁN**\n"
                f"────────────────────────────\n"
                f"🆔 **ID:** {project.id}\n"
                f"📛 **Tên dự án:** {project.name}\n"
                f"📝 **Mô tả:** {project.description or 'Không có mô tả'}\n"
                f"📊 **Trạng thái:** {project.status}\n"
                f"📅 **Ngày bắt đầu:** {project.start_date}\n"
                f"⏳ **Ngày kết thúc:** {project.end_date}\n"
                f"🏢 **Công ty ID:** {project.company_id}\n"
                f"────────────────────────────"
            )
            return result
        except Project.DoesNotExist:
            return "Project not found"

    def _get_all_projects(self) -> str:
        """Get list of all projects"""
        projects = Project.objects.all()
        if not projects:
            return "No projects found"
        
        result = "All Projects:\n"
        for project in projects:
            result += f"- ID: {project.id}, Name: {project.name}, Status: {project.status}, Start: {project.start_date}, End: {project.end_date}\n"
        return result

    def _get_projects_by_user(self, user_id: int) -> str:
        """Get all projects assigned to a specific user"""
        try:
            project_users = ProjectUser.objects.filter(user_id=user_id)
            if not project_users:
                return f"No projects found for user ID: {user_id}"
            
            result = f"Projects for User ID {user_id}:\n"
            for pu in project_users:
                project = pu.project
                result += f"- ID: {project.id}, Name: {project.name}, Role ID: {self._mapping_role_id_to_name(pu.role_id)}, Status: {project.status}\n"
            return result
        except Exception as e:
            return f"Error retrieving projects for user: {str(e)}"

    def _get_project_members(self, project_id: int) -> str:
        """Get all members of a specific project"""
        try:
            project_users = ProjectUser.objects.filter(project_id=project_id)
            if not project_users:
                return f"No members found for project ID: {project_id}"
            
            result = f"Members for Project ID {project_id}:\n"
            for pu in project_users:
                result += f"- User ID: {pu.user_id}, Role ID: {self._mapping_role_id_to_name(pu.role_id)}, Full Name: {pu.user.full_name}\n"
            return result
        except Exception as e:
            return f"Error retrieving project members: {str(e)}"

    # Task-related methods
    def _get_task_info_by_id(self, task_id: int) -> str:
        """Get task information by task ID"""
        try:
            task = Task.objects.get(id=task_id)
            return f"Task Info - ID: {task.id}, Name: {task.task_name}, Description: {task.description}, Work Time: {task.work_time}h, Status ID: {task.status_id}, Priority: {task.priority.name if task.priority else 'None'}, Due Date: {task.due_date}, Project: {task.project.name}"
        except Task.DoesNotExist:
            return "Task not found"

    def _get_tasks_by_project(self, project_id: int) -> str:
        """Get all tasks for a specific project"""
        try:
            tasks = Task.objects.filter(project_id=project_id)
            if not tasks:
                return f"No tasks found for project ID: {project_id}"
            
            result = f"Tasks for Project ID {project_id}:\n"
            for task in tasks:
                result += f"- ID: {task.id}, Name: {task.task_name}, Status: {task.status_id}, Work Time: {task.work_time}h, Due: {task.due_date}\n"
            return result
        except Exception as e:
            return f"Error retrieving tasks: {str(e)}"

    def _get_tasks_by_user(self, user_id: int) -> str:
        """Get all tasks assigned to a specific user"""
        try:
            task_users = TaskUser.objects.filter(user_id=user_id)
            if not task_users:
                return f"No tasks found for user ID: {user_id}"
            
            result = f"Tasks for User ID {user_id}:\n"
            for tu in task_users:
                task = tu.task
                result += f"- ID: {task.id}, Name: {task.task_name}, Status: {task.status_id}, Project: {task.project.name}, Due: {task.due_date}\n"
            return result
        except Exception as e:
            return f"Error retrieving tasks for user: {str(e)}"

    def _get_project_statistics(self, project_id: int) -> str:
        """Get statistics for a specific project"""
        try:
            project = Project.objects.get(id=project_id)
            tasks = Task.objects.filter(project_id=project_id)
            total_tasks = tasks.count()
            completed_tasks = tasks.filter(status_id=3).count()  # Assuming 3 is completed
            total_work_time = sum(task.work_time for task in tasks)
            
            project_users = ProjectUser.objects.filter(project_id=project_id)
            total_users = project_users.count()
            
            completion_rate = (completed_tasks/total_tasks*100) if total_tasks > 0 else 0
            return f"Project Statistics for '{project.name}':\n- Total Tasks: {total_tasks}\n- Completed Tasks: {completed_tasks}\n- Total Work Time: {total_work_time}h\n- Assigned Users: {total_users}\n- Completion Rate: {completion_rate:.1f}%"
        except Project.DoesNotExist:
            return "Project not found"
        except Exception as e:
            return f"Error calculating statistics: {str(e)}"
        
    def create_tools(self):
        return [
            StructuredTool.from_function(
                func=self._get_project_info_by_id,
                name="get_project_info_by_id",
                description="Get detailed project information by project ID",
                args_schema=ProjectIdInput
            ),
            
            Tool(
                name="get_all_projects",
                func=lambda *args, **kwargs: self._get_all_projects(),
                description="Get list of all projects in the system. No input required."
            ),
            
            StructuredTool.from_function(
                func=self._get_projects_by_user,
                name="get_projects_by_user",
                description="Get all projects assigned to a specific user",
                args_schema=UserIdInput
            ),

            StructuredTool.from_function(
                func=self._get_project_members,
                name="get_project_members",
                description="Get all members of a specific project",
                args_schema=ProjectIdInput
            ),
            
            
            StructuredTool.from_function(
                func=self._get_project_statistics,
                name="get_project_statistics",
                description="Get statistics for a specific project",
                args_schema=ProjectIdInput
            ),
            
            
            StructuredTool.from_function(
                func=self._get_tasks_by_project,
                name="get_tasks_by_project",
                description="Get all tasks for a specific project",
                args_schema=ProjectIdInput
            ),
            StructuredTool.from_function(
                func=self._get_tasks_by_user,
                name="get_tasks_by_user",
                description="Get all tasks assigned to a specific user",
                args_schema=UserIdInput
            ),
            
            StructuredTool.from_function(
                func=self._get_task_info_by_id,
                name="get_task_info_by_id",
                description="Get detailed task information by task ID",
                args_schema=TaskIdInput
            ),
            
        ]