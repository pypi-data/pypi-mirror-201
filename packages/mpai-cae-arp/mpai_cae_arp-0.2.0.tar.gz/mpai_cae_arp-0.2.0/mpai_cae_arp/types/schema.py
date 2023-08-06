from pydantic import BaseModel, Field


class Contact(BaseModel):
    name: str = Field(..., description="Name of the contact person.")
    email: str = Field(..., description="Email of the contact person.")

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "email@email.com"
            }
        }


class License(BaseModel):
    name: str = Field(..., description="Name of the license.")
    url: str = Field(..., description="URL of the license.")

    class Config:
        schema_extra = {
            "example": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        }


class Info(BaseModel):
    title: str = Field(..., description="The title of the API.")
    description: str = Field(..., description="A short description of the API.")
    version: str = Field(..., description="The version of the API.")
    contact: Contact = Field(
        ..., description="Contact information for the owners of the API.")
    license_info: License = Field(
        ..., description="License information for the API.")

    class Config:
        schema_extra = {
            "example": {
                "title": "API title",
                "description": "A very nice API",
                "version": "0.1.0",
                "contact": {
                    "name": "John Doe",
                    "email": "example@example.com",
                },
                "license_info": {
                    "name": "MIT",
                    "url": "https://opensource.org/licenses/MIT",
                }
            }
        }
