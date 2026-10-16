from pydantic import BaseModel, ValidationError,Field,field_validator
from fastapi import FastAPI

app=FastAPI()



# 1. Hum ne aik Model (Security Rules) banaya
class Student(BaseModel):
    id: int
    name: str
    age: int
    list : str
    is_active: bool = True  # Default value: agar hum na dein to khud True ho jayega


# dusra concept ya tast 2 3 Models (Schemas
class student2(BaseModel):
    id:int=Field(gt=0,description="enter a student id")
    user_name:str=Field(min_length=1, max_length=14, description="enter a vaild student name", pattern="^[a-zA-Z]")
    @field_validator('user_name')
    def valid_user_name(cls,value):
        if " " in value:
            raise ValueError ("there is space no allow please remove the space")
        return value

    age:int=Field(ge=18, le=50 ,description="this is valide only for the 18+ ")


@app.post("/student")
def student_details(request:Student):
    return {"status":"good execture successfully","Data":request}

@app.post("/student2")
def student_details2(request:student2):
    return {"status":"good anwar test is  successfully","Data":request}

