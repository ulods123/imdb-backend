import os

from flask import Flask,request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from admin.v1.application import admin_blueprint
from user.v1.application import users_v1_blueprint
from helpers import create_error_response,validate_request_body,\
    execute_query,get_hashed_password,create_success_response
from custom_exceptions import DatabaseException,BadRequestException, \
    AuthError
from auth.auth import create_token,login_required,check_scope

app=Flask(__name__,static_folder='docs')
CORS(app)

STATIC_PATH = os.path.join(os.getcwd(),'docs')
print(STATIC_PATH)

app.register_blueprint(admin_blueprint,url_prefix='/api/admin/v1')

app.register_blueprint(users_v1_blueprint,url_prefix='/api/user/v1')

swaggerui_blueprint = get_swaggerui_blueprint(
    "/api/docs",  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    "/docs/swagger.json"
)

app.register_blueprint(swaggerui_blueprint)

@app.errorhandler(DatabaseException)
def handle_auth_error(ex):
    return create_error_response(error_code="DATABASE_ERROR",error_message=ex.error,status_code=502)

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return create_error_response(error_code="UNAUTHORIZED",error_message=ex.error,status_code=ex.status_code)

@app.errorhandler(BadRequestException)
def handle_auth_error(ex):
    return create_error_response(error_code="BAD_REQUEST",error_message=ex.error,status_code=400)

@app.errorhandler(Exception)
def handle_auth_error(ex):
    return create_error_response()


@app.route('/health',methods=['GET'])
def health():
    return "Yo I am running!!!"

@app.route('/api/testToken',methods=['POST'])
@login_required
@check_scope(scope_required="create")
def test():
    return "Yo I am running!!!"


@app.route('/api/getToken',methods=['POST'])
def get_token():
    request_body=request.json
    validate_request_body('login',request_body)
    query=f"call get_password(@email_id:='{request_body['emailid']}')"
    print(query)
    result=execute_query(query)
    print(result)
    if isinstance(result,dict) and result['password'] == get_hashed_password(request_body['password']):
        query=f"call get_scopes(@email_id:='{request_body['emailid']}')"
        print(query)
        result=execute_query(query)
        print(result)
        response={}
        if isinstance(result,list):
            response['token']=create_token([row["name"] for row in result])
        elif isinstance(result,dict):
            response['token']=create_token([result["name"]])
        else:
            response['token']=create_token([])
        return create_success_response(response)
    else:
        raise AuthError("Invalid Credentials",403)



if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)