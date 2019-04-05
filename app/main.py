from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@127.0.0.1:5432/techcamp_projectmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 's0meSecretKey'
db = SQLAlchemy(app=app)
import resources

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(resources.Users,'/users')
api.add_resource(resources.User,'/users/<int:id>')
api.add_resource(resources.Projects,'/projects')
api.add_resource(resources.Project,'/projects/<int:id>')
api.add_resource(resources.Homepage,'/')














