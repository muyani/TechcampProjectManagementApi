from main import db

class ProjectsModel(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120),nullable=False,unique=True)
    description = db.Column(db.String(),nullable=True)
    startDate = db.Column(db.DateTime,nullable=False)
    endDate = db.Column(db.DateTime,nullable=False)
    cost = db.Column(db.Float,nullable=False)
    status = db.Column(db.String(30))
    userId =  db.Column(db.Integer,db.ForeignKey('users.id'))

    # CREATE
    def create_record(self):
        db.session.add(self)
        db.session.commit()

    # READ
    @classmethod
    def fetch_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'title': x.title,
                'description': x.description,
                'startDate': str(x.startDate),
                'endDate': str(x.endDate),
                'cost': x.cost,
                'status': x.status,
                'user': x.user.username
            }
        return {'projects': list(map(lambda x: to_json(x), cls.query.all()))}

    @classmethod
    def fetch_by_title(cls,title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def fetch_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    #UPDATE
    @classmethod
    def update_by_id(cls,id,newTitle,newDescription,newStartDate,newEndDate,newCost,newStatus,newUserId):
        record = ProjectsModel.query.filter_by(id=id).first()
        if record:
            record.title = newTitle
            record.description = newDescription
            record.startDate = newStartDate
            record.endDate = newEndDate
            record.cost = newCost
            record.status = newStatus
            record.userId = newUserId
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
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'},500


class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),nullable=False,unique=True)
    projects = db.relationship('ProjectsModel',backref = 'user')

    # CREATE
    def create_record(self):
        db.session.add(self)
        db.session.commit()

    # READ
    @classmethod
    def fetch_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'username': x.username
            }
        return {'projects': list(map(lambda x: to_json(x), cls.query.all()))}

    @classmethod
    def fetch_projects_by_id(cls,id):
        record = cls.query.filter_by(id=id).first()
        def to_json(x):
            return {
                'id': x.id,
                'title': x.title,
                'description': x.description,
                'startDate': str(x.startDate),
                'endDate': str(x.endDate),
                'cost': x.cost,
                'status': x.status,
                'user': x.user.username
            }
        return {'projects': list(map(lambda x: to_json(x), record.projects))}

    @classmethod
    def fetch_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    #UPDATE
    @classmethod
    def update_by_id(cls,id,newUsername):
        record = ProjectsModel.query.filter_by(id=id).first()
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





