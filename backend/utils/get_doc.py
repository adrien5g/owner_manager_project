from flask_pydantic_openapi import FlaskPydanticOpenapi

class Doc(FlaskPydanticOpenapi):

    def __init__(self,backend_str: str = 'base', *args, **kwargs):
        super().__init__(backend_str,*args, **kwargs)

doc = FlaskPydanticOpenapi("AHP")

def get_doc() -> FlaskPydanticOpenapi:
    return doc