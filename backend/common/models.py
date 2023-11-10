from .database import db
from sqlalchemy import func

roles_users = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable = False),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)    
    email = db.Column(db.String(55), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean(), nullable = False, default=True)
    role = db.relationship('Role', secondary=roles_users, backref=db.backref('users'))
    created_at = db.Column(db.String(), default=func.now())
    completed_courses = db.relationship('CoursesCompleted', backref=db.backref('users', lazy='dynamic'))

    def create(self):
        pass

    def delete(self):
        pass

    def is_active(self):
        pass

    def what_role(self):
        pass

    def __repr__(self):
        return f'{self.id}, {self.email} |'

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key = True)
    role = db.Column(db.String(55), unique = True, nullable = False)
    description = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return f'{self.id}, {self.role} |'

class Courses(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    difficulty_rating = db.Column(db.Float)
    co_requisites = db.relationship('Courses')
    pre_requisites = db.relationship('Courses')


class CoursesCompleted(db.Model):
    __tablename__ = 'users_courses'
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    marks = db.Column(db.Float, nullable=False),
    completed = db.Column(db.Boolean, default=False)

class Recommendations(db.Model):
    __tablename__ = 'recommend'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    time = db.Column(db.String(), default=func.now())