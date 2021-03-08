from flask import Blueprint,request,jsonify,current_app


admin_blueprint=Blueprint('admin',__name__)


@admin_blueprint.route('/health',methods=['GET'])
def health():
    return "Yo from Admin"