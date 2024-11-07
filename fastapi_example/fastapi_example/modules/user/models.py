from pydantic import BaseModel, EmailStr, SecretStr


class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
