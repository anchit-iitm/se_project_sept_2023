from .database import db
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

roles_users = db.Table('user_roles',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable = False),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )

Users_Courses = db.Table('user_courses',
        db.Column('id', db.Integer, primary_key=True, autoincrement=True, nullable=False),
        db.Column('user', db.Integer, db.ForeignKey('user.id'), nullable=False),
        db.Column('course', db.String(10), db.ForeignKey('courses.code'), nullable=False),
        db.Column('marks', db.Float, nullable=False),
        db.Column('completed', db.Boolean, default=False),    
    )


Courses_Instructors = db.Table('courses_intructors',
        db.Column('user', db.Integer, db.ForeignKey('user.id'), nullable=False),
        db.Column('course', db.String(10), db.ForeignKey('courses.code')),
    )


# class Course_Coreqs(db.Model):
#         course_code = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
#         coreq_code = db.Column(db.String(10), db.ForeignKey('courses.code'))

# Course_Prereqs = db.Table('courses_prereqs', 
#         db.Column('course_code', db.String(10), db.ForeignKey('courses.code'), nullable=False),
#         db.Column('prereq_code', db.String(10), db.ForeignKey('courses.code')),
#     )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(55), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean(), nullable = False, default=True)

    pic = db.Column(db.String(500), nullable=True)
    max_subjects = db.Column(db.Integer, default=0)
    curr_deg_level = db.Column(db.String(10), nullable=True)
    ds_or_dp = db.Column(db.String(10), nullable=True)

    role = db.relationship('Role', secondary=roles_users, backref=db.backref('user'))
    created_at = db.Column(db.String(), default=func.now())
    completed_courses = db.relationship('Courses', secondary=Users_Courses, backref=db.backref('user'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.id}, {self.email} |'

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key = True, autoincrement=True)
    role = db.Column(db.String(55), unique = True, nullable = False)
    description = db.Column(db.String(255), nullable = False)

    @classmethod
    def stu_role(cls):
        return cls.query.filter_by(role='student').first()
    
    @classmethod
    def admin_role(cls):
        return cls.query.filter_by(role='admin').first()

    def __repr__(self):
        return f'{self.id}, {self.role} |'



class Courses(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    difficulty_rating = db.Column(db.Float)
    level = db.Column(db.String(10), nullable=False)
    instructors = db.relationship('User', secondary=Courses_Instructors, backref=db.backref('courses'))

    #co_requisites = db.relationship('Courses', secondary = Course_Coreqs, foreign_keys='[Course_Coreqs.course_code]')
    #pre_requisites = db.relationship('Courses', secondary = Course_Prereqs, foreign_keys='[courses_prereqs.course_code]')


class Recommendations(db.Model):
    __tablename__ = 'recommend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('courses.code'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    time = db.Column(db.String(), default=func.now())
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)