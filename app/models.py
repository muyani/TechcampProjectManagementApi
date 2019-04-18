from main import db
from datetime import datetime

class ProjectsModel(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(),nullable=False,unique=True)
    description = db.Column(db.String(),nullable=True)
    createdDate = db.Column(db.DateTime,nullable=False,default = datetime.now)
    startDate = db.Column(db.DateTime,nullable=True)
    endDate = db.Column(db.DateTime,nullable=True)
    status = db.Column(db.Integer)
    userId = db.Column(db.Integer,db.ForeignKey('users.id'))

    # CREATE
    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # READ
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_title(cls,title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def fetch_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    #UPDATE
    @classmethod
    def update_by_id(cls,id,newTitle,newDescription,newStartDate,newEndDate,newStatus):
        record = ProjectsModel.query.filter_by(id=id).first()
        if record:
            record.title = newTitle
            record.description = newDescription
            record.startDate = newStartDate
            record.endDate = newEndDate
            record.status = newStatus
            db.session.commit()
            return True
        else:
            return False

    #DELETE
    @classmethod
    def delete_by_id(cls,id):
        record = ProjectsModel.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def delete_all(cls,id):
        try:
            records = cls.query.filter_by(userId = id)
            if records.all():
                records.delete()
                db.session.commit()
            return True
        except:
            return False

class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),nullable=False,unique=True)
    projects = db.relationship('ProjectsModel',backref = 'user')

    # CREATE
    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # READ
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    #UPDATE
    @classmethod
    def update_by_id(cls,id,newUsername):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.username = newUsername
            db.session.commit()
            return True
        else:
            return False

    #DELETE
    @classmethod
    def delete_by_id(cls,id):
        record = cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False





