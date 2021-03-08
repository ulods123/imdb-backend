from flask import Flask


from admin.v1.application import admin_blueprint
from user.v1.application import users_v1_blueprint
from helpers import create_error_response
from custom_exceptions import DatabaseException,BadRequestException

app=Flask(__name__)


app.register_blueprint(admin_blueprint,url_prefix='/api/admin/v1')

app.register_blueprint(users_v1_blueprint,url_prefix='/api/user/v1')

@app.errorhandler(DatabaseException)
def handle_auth_error(ex):
    return create_error_response(error_code="DATABASE_ERROR",error_message=ex.error,status_code=502)

@app.errorhandler(BadRequestException)
def handle_auth_error(ex):
    return create_error_response(error_code="BAD_REQUEST",error_message=ex.error,status_code=400)

# @app.errorhandler(Exception)
# def handle_auth_error(ex):
#     return create_error_response()



@app.route('/health',methods=['GET'])
def health():
    return "Yo I am running!!!"


if __name__=="__main__":
    app.run(host="0.0.0.0")