from pydantic import EmailStr
from fastapi.param_functions import Form


class SignUpRequestForm:

    def __init__(
        self,
            email: EmailStr = Form(...),
            password: str = Form(...),
            first_name: str = Form(...),
            last_name: str = Form(...)
    ):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
