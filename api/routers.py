import pymongo
from fastapi import APIRouter # Import ApiRouter class from fastapi
from api.ProjectManager import HWC_Project, MongoDB_Manager

HWC = HWC_Project()
MongoDB = MongoDB_Manager()

router = APIRouter(
    prefix = "", # Set the prefix of the router
    tags = [""], # Set the tag of the router
    responses = {404: {"description": "Not Found"}}, #set the 404 response
) # Initialize the router

@router.get('/') # Index route
async def get_all_projects():
    list = HWC.getAllProjects()
    data = {}
    return data

@router.get('viewer/{id}') 
async def get(id):
    list = HWC.getProject(id)
    data = {}
    return data



@router.get('admin/{id}') 
async def get(id):
    list = HWC.getProject(id)
    data = {}
    return data
