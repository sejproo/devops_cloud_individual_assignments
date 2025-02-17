import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


""" def add(student=None):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return 'not found', 404
    student_db.remove(doc_ids=[int(student_id)])
    return student_id """

# pymongo implementation

import pymongo
import uuid

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
myclient = pymongo.MongoClient(mongo_uri)
mydb = myclient["mydatabase"]
student_db = mydb["students"]


def add(student=None):
    if not student:
        return 'error', 400
    
    exists = student_db.find_one({
        "first_name": student.first_name, 
        "last_name": student.last_name
    })
    
    if exists:
        return 'already exists', 409
    
    new_uuid = str(uuid.uuid4())
    
    student_dict = student.to_dict()
    student_dict['_id'] = new_uuid
    
    student_db.insert_one(student_dict)
    return new_uuid

    
def get_by_id(student_id=None, subject=None):
    
    if not student_id:
        return 'invalid', 400
    student = student_db.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    return student
    


def delete(student_id=None):
        
    if not student_id:
        return 'error', 400
    student = student_db.find_one({"id": student_id})
    if not student:
        return 'not found', 404
    student_db.delete_one({"id": student_id})
    return student_id