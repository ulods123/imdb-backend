

from flask import Blueprint,request,jsonify,current_app

from helpers import create_success_response, \
    validate_request_body,execute_query

from custom_exceptions import BadRequestException

users_v1_blueprint=Blueprint('users_v1',__name__)


@users_v1_blueprint.route('/',methods=['GET'])
def fetch_data():
    data=request.args
    if data:
        is_valid,error=validate_request_body('fetch_movies',data)
        if not is_valid:
            raise BadRequestException(error)
    start_after=(int(data.get('page',1))*10)-10
    query=f"call get_movies(@start_after:={start_after},@limit:=10)"
    print(query)
    result=execute_query(query)
    response={}
    if isinstance(result,list):
        response['total_count']=result[0]['total_count'] 
        for row in result:
            del row['total_count']
    else:  
        response['total_count']=result['total_count']
        del result['total_count']
    response['display_data']=result
    return create_success_response(response)


@users_v1_blueprint.route('/<type>',methods=['GET'])
def fetch_data_by_filter(type):
    data=request.args
    is_valid,error=validate_request_body('fetch_movies_genre',data)
    if not is_valid:
        raise BadRequestException(error)
    start_after=(int(data.get('page',1))*10)-10
    if type=="genre":
        query=f"call get_movies_by_genre(@start_after:={start_after},@limit:=10,@genre:='{data['filter']}')"
    elif type=="director":
        query=f"call get_movies_by_director(@start_after:={start_after},@limit:=10,@director:='{data['filter']}')"
    print(query)
    result=execute_query(query)
    print(result)
    response={}
    if isinstance(result,list):
        response['total_count']=result[0]['total_count'] 
        for row in result:
            del row['total_count']
    elif isinstance(result,dict):  
        response['total_count']=result['total_count']
        del result['total_count']
    response['display_data']=result
    return create_success_response(response)

@users_v1_blueprint.route('/getGenre/<movie_id>',methods=['GET'])
def get_genre_for_movie(movie_id):
    query=f"call get_genre_of_movie(@movie_id:={movie_id})"
    result=execute_query(query)
    return create_success_response(result)