from pydantic import BaseModel, ConfigDict, Field, SecretStr


class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=255)
    password: SecretStr = Field(min_length=6)


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    username: str
    email: str


class Message(BaseModel):
    message: str


class RegistrationResponse(BaseModel):
    success: bool
    message: str
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
