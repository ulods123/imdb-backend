#python default imports
import json
from datetime import datetime
import hashlib

#pip install imports
from flask import jsonify
import pymysql
from pymysql import OperationalError,ProgrammingError
from cerberus import Validator

# application imports
from config import Config
from custom_exceptions import DatabaseException,BadRequestException

def create_success_response(data={}):
        row=jsonify(responseStatus="SUCCESS",data=data)
        row.status_code=200
        return row


def create_error_response(error_code="INTERNAL_SERVER_ERROR",error_message="Something went wrong",status_code=500):
        row=jsonify(responseStatus="ERROR",error={"errorCode":error_code,"errorMessage":error_message})
        row.status_code=status_code
        return row


def create_scope_error_response():
    return create_error_response(error_code="UNAUTHORIZED",error_message="user is not allowed to perform this action",status_code=401)

def get_database_connection():
    return pymysql.connect(host=Config.Database.SERVER_NAME,user=Config.Database.USER,password=Config.Database.PASSWORD,database=Config.Database.DATABASE_NAME)



def execute_query(query,cursor_class=pymysql.cursors.DictCursor):
    connection=get_database_connection()
    cursor=connection.cursor(cursor_class)
    try:
        cursor.execute(query)
        if cursor.rowcount==1:
            row=cursor.fetchone()
        else:
            row=cursor.fetchall()
        return row
    except (OperationalError,ProgrammingError) as e:
        print(e)
        raise DatabaseException(e.args[1])
    finally:
        connection.commit()
        cursor.close()
        connection.close()

def validate_request_body(schema_file_name,request_body):
    v = Validator(read_schema_file(schema_file_name))
    valid = v.validate(request_body)
    if not valid:
        raise BadRequestException(v.errors)

def read_schema_file(schema_file_name):
    with open(f'requestschemas/{schema_file_name}.json') as f:
        return json.loads(f.read())  

def get_hashed_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

