from flask import Flask,request,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, reqparse, fields, marshal
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@172.17.0.1:5432/techcamp_projectmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 's0meSecretKey'

app.config['RESTPLUS_VALIDATE'] = True
db = SQLAlchemy(app=app)
from models import ProjectsModel,UsersModel

api = Api(app)

ns = api.namespace('api/v1',description='Techcamp Task Management System operations.')


@app.errorhandler(400)
def badRequest(e):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def notFound(e):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@app.errorhandler(405)
def notAllowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@app.errorhandler(500)
def internalServer(e):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

# Request parsing

userParser = reqparse.RequestParser()
userParser.add_argument('username', type=str, help='Username ',required= True)

projectParser = reqparse.RequestParser()
projectParser.add_argument('title', type=str, help='Title of the task',required= True)
projectParser.add_argument('description', type=str, help='Description of the task',required= True)


projectUpdateParser = reqparse.RequestParser()
projectUpdateParser.add_argument('title', type=str, help='Title of the task',required= True)
projectUpdateParser.add_argument('description', type=str, help='Description of the task',required= True)
projectUpdateParser.add_argument('status', type=int, help='0 if todo,1 if ongoing,2 if complete',required= True)


# Response marshalling
project = api.model('Project', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'createdDate': fields.DateTime,
    'startDate': fields.DateTime,
    'endDate': fields.DateTime,
    'status': fields.Integer
})

userStructure = api.model('user',{
    'id':fields.String,
    'username':fields.String
})

@app.before_first_request
def create_tables():
    db.create_all()

def conflict(title):
    return {'Record {} already exists'.format(title)},409

@ns.route('/tasks/<int:uid>')
@ns.response(200, 'Success')
@ns.response(201, 'Record Created Successfuly')
@ns.response(204, 'Record Deleted Successfuly')
@ns.response(400, 'Not valid request body')
@ns.response(404, 'Resource not found')
@ns.response(409, 'Record Already exists')
@ns.response(500, 'Server Error')
class Projects(Resource):
    @ns.expect(projectParser)
    @ns.marshal_with(project)
    def post(self,uid):
        args = projectParser.parse_args()
        dateformat = '%Y-%m-%d'
        title = args['title']
        description = args['description']
        status = 0
        userId = uid
        if UsersModel.fetch_by_id(uid) == None:
            return {"message":"User not found"},404
        if ProjectsModel.fetch_by_title(title):
            return 'project "{}" already exist'.format(title),409
        project = ProjectsModel(title=title, description=description,status=status,userId=userId)
        record = project.create_record()
        print(record)
        return record, 201

    def get(self,uid):
        user = UsersModel.fetch_by_id(uid)
        try:
            record = user.projects
            if record:
                return marshal(record,project), 200
            return {}, 404
        except:
            return {"Message":"User does not exist"},404

    def delete(self,uid):
        deleted = ProjectsModel.delete_all(uid)
        if deleted:
            return {'Message':'Records Deleted Successfully'},204
        else:
            return {'Message':'Something is wrong with the server'},500


@ns.route('/users')
@ns.response(200, 'Success')
@ns.response(201, 'Record Created Successfuly')
@ns.response(204, 'Record Deleted Successfuly')
@ns.response(400, 'Not valid request body')
@ns.response(404, 'Resource not found')
@ns.response(409, 'Record Already exists')
@ns.response(500, 'Server Error')
class Users(Resource):
    @ns.expect(userParser)
    def post(self):
        args = userParser.parse_args()
        username = args['username']
        username = username.lower()
        user = UsersModel.fetch_by_username(username)
        if user:
            return marshal(user, userStructure), 200
        user = UsersModel(username=username)
        record = user.create_record()
        return marshal(record,userStructure),201

@ns.route('/tasks/<int:uid>/<int:pid>')
@ns.response(200, 'Success')
@ns.response(201, 'Record Created Successfuly')
@ns.response(204, 'Record Deleted Successfuly')
@ns.response(400, 'Not valid request body')
@ns.response(404, 'Resource not found')
@ns.response(409, 'Record Already exists')
@ns.response(500, 'Server Error')
class Project(Resource):
    @ns.expect(projectUpdateParser)
    @ns.marshal_with(project)
    def put(self,uid,pid):
        user = UsersModel.fetch_by_id(uid)
        record = user.projects
        for each in record:
            if each.id == pid:
                body = projectUpdateParser.parse_args()
                title = body['title']
                description = body['description']
                status = int(body['status'])
                startDate = None
                endDate = None
                if status == 1:
                    startDate = datetime.now()
                elif status == 2:
                    endDate = datetime.now()
                updated = ProjectsModel.update_by_id(id=pid, newTitle=title, newDescription=description,
                                                     newStartDate=startDate, newEndDate=endDate,
                                                     newStatus=status)

                if updated:
                    record = ProjectsModel.fetch_by_id(pid)
                    return record,200
                else:
                    return {},400

        return {},404

    def get(self,uid,pid):
        user = UsersModel.fetch_by_id(uid)
        try:
            record = user.projects
            for each in record:
                if each.id == pid:
                    return marshal(each, project), 200
            return {}, 404
        except:
            return {"Message":"User not found"},500

    def delete(self,uid,pid):
        user = UsersModel.fetch_by_id(uid)
        record = user.projects
        for each in record:
            if each.id == pid:
                deleted = ProjectsModel.delete_by_id(pid)
                if deleted:
                    return {"Message": "Task deleted Successfully"}, 204
                return {"Message":"something went wrong"},500
        return {"Message":"Record not found"},404

@ns.route('/users/<int:uid>')
@ns.response(200, 'Success')
@ns.response(201, 'Record Created Successfuly')
@ns.response(204, 'Record Deleted Successfuly')
@ns.response(400, 'Not valid request body')
@ns.response(404, 'Resource not found')
@ns.response(409, 'Record Already exists')
@ns.response(500, 'Server Error')
class User(Resource):
    @ns.expect(userParser)
    def put(self,uid):
        args = userParser.parse_args()
        username = args['username'].lower()
        if UsersModel.fetch_by_username(username):
            return {"message":"Username {} already exists".format(username)},409
        updated = UsersModel.update_by_id(id=uid, newUsername=username)
        if updated:
            record = UsersModel.fetch_by_id(uid)
            return marshal(record,userStructure),200
        else:
            return {"Message":"Record not updated"},500

    def get(self,uid):
        record = UsersModel.fetch_by_id(uid)
        if record:
            return marshal(record,userStructure),200
        else:
            return {"message":"Not found"},404

@ns.route('/')
class Homepage(Resource):
    def get(self):
        return {"Message":"Welcome to Techcamp Task Management Api"},200
    def post(self):
        return {"Message": "Welcome to Techcamp Task Management Api"},200





