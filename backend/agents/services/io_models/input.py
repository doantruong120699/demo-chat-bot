from pydantic import BaseModel, Field
from typing import Optional

class UserSearchInput(BaseModel):
    """Input for user search operations"""
    email: Optional[str] = Field(description="Email address of the user")
    user_id: Optional[int] = Field(description="ID of the user")
    full_name: Optional[str] = Field(description="Full name of the user")


class ProjectSearchInput(BaseModel):
    """Input for project search operations"""
    project_id: Optional[int] = Field(description="ID of the project")
    name: Optional[str] = Field(description="Name of the project")
    company_id: Optional[int] = Field(description="Company ID")


class TaskSearchInput(BaseModel):
    """Input for task search operations"""
    task_id: Optional[int] = Field(description="ID of the task")
    project_id: Optional[int] = Field(description="ID of the project")
    user_id: Optional[int] = Field(description="ID of the assigned user")
    status_id: Optional[int] = Field(description="Status ID of the task")


class TimeIntervalSearchInput(BaseModel):
    """Input for time interval search operations"""
    time_interval_id: Optional[int] = Field(description="ID of the time interval")
    task_id: Optional[int] = Field(description="ID of the task")
    user_id: Optional[int] = Field(description="ID of the user")


class NotificationSearchInput(BaseModel):
    """Input for notification search operations"""
    user_id: int = Field(description="ID of the user")
    is_seen: Optional[bool] = Field(description="Whether notification is seen")
    status: Optional[str] = Field(description="Status of notification: 'unread' or 'ready'")


class UserIdInput(BaseModel):
    """Input for operations requiring only user ID"""
    user_id: int = Field(description="ID of the user")


class ProjectIdInput(BaseModel):
    """Input for operations requiring only project ID"""
    project_id: int = Field(description="ID of the project")


class TaskIdInput(BaseModel):
    """Input for operations requiring only task ID"""
    task_id: int = Field(description="ID of the task")


class TimeIntervalIdInput(BaseModel):
    """Input for operations requiring only time interval ID"""
    time_interval_id: int = Field(description="ID of the time interval")


class EmailInput(BaseModel):
    """Input for operations requiring email"""
    email: str = Field(description="Email address of the user")


class LogLimitInput(BaseModel):
    """Input for log operations with limit"""
    user_id: int = Field(description="ID of the user")
    limit: int = Field(default=10, description="Number of logs to retrieve (default: 10)")

class DateRangeInput(BaseModel):
    """Input for operations requiring date range"""
    start_date: str = Field(description="Start date in format YYYY-MM-DD")
    end_date: str = Field(description="End date in format YYYY-MM-DD")


class DateRangeInputByUser(BaseModel):
    """Input for operations requiring date range by user"""
    user_id: int = Field(description="ID of the user")
    start_date: str = Field(description="Start date in format YYYY-MM-DD")
    end_date: str = Field(description="End date in format YYYY-MM-DD")


class UserFilterInput(BaseModel):
    """Input for getting projects by user with flexible identification"""
    user_id: Optional[int] = Field(None, description="ID of the user")
    email: Optional[str] = Field(None, description="Email address of the user")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    
    class Config:
        # At least one field must be provided
        @staticmethod
        def validate_at_least_one_field(cls, values):
            if not any(values.values()):
                raise ValueError("At least one of user_id, email, or full_name must be provided")
            return values
        
class ProjectFilterInput(BaseModel):
    """Input for getting projects by user with flexible identification"""
    project_id: Optional[int] = Field(None, description="ID of the project")
    project_name: Optional[str] = Field(None, description="Name of the project")
    
    class Config:
        # At least one field must be provided
        @staticmethod
        def validate_at_least_one_field(cls, values):   
            if not any(values.values()):
                raise ValueError("At least one of project_id, project_name must be provided")
            return values


class ProjectChartInput(BaseModel):
    """Input for getting project chart"""
    project_id: int = Field(description="ID of the project")