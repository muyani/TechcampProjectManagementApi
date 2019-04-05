from flask_restful import Resource
from flask import request
from models import ProjectsModel,UsersModel
from datetime import datetime

class Projects(Resource):
    def post(self):
        if request.is_json:
            body = request.get_json()
            dateformat = '%Y-%b-%d %H:%M'
            try:
                title = body['title']
                description = body['description']
                startDate = body['startDate']
                endDate = body['endDate']
                cost = body['cost']
                status = body['status']
                startDate = datetime.strptime(startDate,dateformat)
                endDate = datetime.strptime(endDate,dateformat)
            except Exception as e:
                return {"Message":"Invalid JSON Body fields"},400

            if ProjectsModel.fetch_by_title(title):
                return {"Message":"Title {} already exists".format(title)},409

            project = ProjectsModel(title=title, description=description, startDate=startDate,
                                   endDate=endDate, cost=cost, status=status)
            project.create_record()
            return {"Message":"{} created Successfully".format(title)},201
        else:
            return {"Message":"Request Body is not valid JSON"},400

    def get(self):
        records = ProjectsModel.fetch_all()
        return records

    def delete(self):
        return ProjectsModel.delete_all()

class Users(Resource):
    def post(self):
        if request.is_json:
            body = request.get_json()
            try:
                username = body['username']
            except Exception as e:
                return {"Message":"Invalid JSON Body fields"},400

            if UsersModel.fetch_by_username(username):
                return {"Message":"Username {} is already taken".format(username)},409
            user = UsersModel(username=username)
            user.create_record()
            return {"Message":"{} created Successfully".format(username)},201
        else:
            return {"Message":"Request Body is not valid JSON"},400

class Project(Resource):
    def put(self,id):
        record = ProjectsModel.fetch_by_id(id)
        if request.is_json:
            body = request.get_json()
            try:
                title = body['title']
                description = body['description']
                startDate = body['startDate']
                endDate = body['endDate']
                cost = body['cost']
                status = body['status']
            except Exception as e:
                return {"Message":"One or more of the fields are empty" },400

            updated = ProjectsModel.update_by_id(id=id, newTitle=title, newDescription=description,
                                                 newStartDate=startDate, newEndDate=endDate, newCost=cost,
                                                 newStatus=status)
            if updated:
                return {"Message":"{} updated Successfully".format(title)},200
            else:
                return {"Message":"Record not updated"},500

            project = ProjectsModel(title=title, description=description, startDate=startDate,
                                   endDate=endDate, cost=cost, status=status)

            project.create_record()

        else:
            return {"Message":"Request Body is not valid JSON"},400

    def get(self,id):
        record = ProjectsModel.fetch_by_id(id)
        if record:
            return {"id": record.id, "title": record.title, "description": record.description,
                    "startDate": str(record.startDate),
                    "endDate": str(record.endDate), "cost": record.cost, "status": record.status},200
        else:
            return {},404


    def delete(self,id):
        deleted = ProjectsModel.delete_by_id(id)
        if deleted:
            return {"Message":"Project deleted Successfully"},200
        else:
            return {"Message":"Record Not deleted"},500



class User(Resource):
    def put(self,id):
        record = UsersModel.fetch_by_id(id)
        if request.is_json:
            body = request.get_json()
            try:
                username = body['username']
            except Exception as e:
                return {"Message":"One or more of the fields are empty" },400

            updated = UsersModel.update_by_id(id=id, newUsername=username)
            if updated:
                return {"Message":"{} updated Successfully".format(username)},200
            else:
                return {"Message":"Record not updated"},500

        else:
            return {"Message":"Request Body is not valid JSON"},400

    def get(self,id):
        record = UsersModel.fetch_by_id(id)
        if record:
            return {"id": record.id, "username": record.username},200
        else:
            return {},404

class Homepage(Resource):
    def get(self):
        return {"Message":"Welcome to Techcamp Project Management Api"},200
    def post(self):
        return {"Message": "Welcome to Techcamp Project Management Api"},200










