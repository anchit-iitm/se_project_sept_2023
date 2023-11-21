from flask_restful import Resource
from flask import jsonify
from app import api
from common.models import User, Course

class CourseResource(Resource):
    def get(self):
        try:
            courses = Course.query.all()

            if not courses:
                return jsonify({'message': 'No courses found'}), 404

            courses_data = [
                {
                    'id': course.code,
                    'name': course.name,
                    'description': course.description,
                    'difficulty_rating': course.difficulty_rating,
                    'level': course.level,
                    'pre_req': [prerequisite.code for prerequisite in course.pre_requisites],
                    'co_req': [corequisite.code for corequisite in course.co_requisites],
                    'availability': [availability for availability in course.availability],
                    'instructors': [
                        {'name': instructor.name, 'email': instructor.email}
                        for instructor in course.instructors
                    ]
                }
                for course in courses
            ]

            return jsonify({'courses': courses_data}), 200

        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def patch(self, id):
        return jsonify({"message": "Modify single course info by ID"})

    def delete(self, id):
        return jsonify({"message": "Delete single course by ID"})

class CoursesResource(Resource):
    def get(self):
        return jsonify({"message": "Get all courses info"})

    def post(self):
        return jsonify({"message": "Add a new course"})

api.add_resource(CourseResource, '/course/<int:id>')
api.add_resource(CoursesResource, '/courses')