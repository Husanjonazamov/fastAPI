from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel



class PackageIn(BaseModel):
    secret_key: int
    name: str
    number: str
    description: Optional[str] = None



class Package(BaseModel):
    name: str
    number: str
    description: Optional[str] = None


app = FastAPI()

@app.get("/")
async def hello_world():
    return {"Hello": "World"}




@app.get("/packages/{priority}")
async def packages(priority: int, package: Package, value: bool):
    return {'priority': priority, **package.dict(), 'value': value}



@app.post("/packages/", response_model=Package, response_model_include={'description'})
async def create_package(package: Package):
    return package


# @app.get("/component/{component_id}")
# async def get_component(component_id: int):
#     return {'component_id': component_id}
#
#
#
# @app.get("/component/")
# async def read_component(number: int, text: Optional[str]):
#     return {'number': number, 'text': text}