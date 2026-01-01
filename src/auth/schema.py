
from pydantic import BaseModel, Field,ConfigDict
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    username:str = Field(max_length=8)
    email:str = Field(max_length=40)
    password:str = Field(min_length=3)
    first_name:str = Field(min_length=3)
    last_name:str= Field(min_length=3)
    
    
class UserResponse(BaseModel):
    uid:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool
    created_at:datetime
    updated_at:datetime
    
    
    
    
    # Pydantic v2 configuration
    model_config = ConfigDict(
        # Use enum values instead of enum names
        use_enum_values=True,
        # Validate assignment (check types when assigning to model instances)
        validate_assignment=True,
        # Serialize datetime and UUID properly
        json_encoders={
            datetime: lambda v: v.isoformat(),  # Convert datetime to ISO format
            uuid.UUID: lambda v: str(v),  # Convert UUID to string
        },
        # Example data for API documentation
        json_schema_extra={
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "username": "arun",
                "email": "arun@gmail.com",
                "first_name": "arun",
                "last_name": "kumar",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
    )