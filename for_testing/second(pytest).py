from pydantic import BaseModel , ValidationError , Field , field_validator  
import pytest

class student (BaseModel):
    age:int=Field(ge=18,le=55,description="this for 18+ only ")
    name:str
    user_name:str=Field(min_length=4,max_length=20)

    @field_validator("user_name")
    def valide_user_name(cls,Value):
        if " " in Value:
            raise ValueError("space not allow " )
        return Value


# pytest 
def test_valid_student():
    s = student(age=2, name="Anwar Ali", user_name="anwar123")
    assert s.user_name == "anwar123"
    assert s.age == 20

