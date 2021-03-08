from flask import Blueprint,request,jsonify,current_app

from helpers import validate_request_body,create_success_response, \
    execute_query

from auth.auth import login_required,check_scope

admin_blueprint=Blueprint('admin',__name__)


@admin_blueprint.route('/',methods=['POST'])
@login_required
@check_scope(scope_required="create")
def insert_movie():
    request_body=request.get_json()
    validate_request_body('insert_movie',request_body)
    query=(f"call insert_movie_data(@name:='{request_body['name']}',"
            f"@director:='{request_body['director']}',"
            f"@popularity:={request_body['popularity']},"
            f"@imdb_score:={request_body['imdb_score']})")
    print(query)
    result=execute_query(query)
    for row in request_body['genre']:
        query=f"call map_movie_to_genre(@movie_id:={result['movie_id']},@genre:='{row}')"
        print(query)
        execute_query(query)
    return create_success_response()




@admin_blueprint.route('/',methods=['PUT'])
@login_required
@check_scope(scope_required="update")
def update_movie():
    request_body=request.get_json()
    validate_request_body('update_movie',request_body)
    query=(f"call update_movie_data(@id:='{request_body['id']}',"
            f"@name:='{request_body['name']}',"
            f"@director:='{request_body['director']}',"
            f"@popularity:={request_body['popularity']},"
            f"@imdb_score:={request_body['imdb_score']})")
    print(query)
    execute_query(query)
    query=f"call delete_movie_genre_mapping(@id:={request_body['id']})"
    print(query)
    execute_query(query)
    for row in request_body['genre']:
        query=f"call map_movie_to_genre(@movie_id:={request_body['id']},@genre:='{row}')"
        print(query)
        execute_query(query)
    return create_success_response()

@admin_blueprint.route('/',methods=['DELETE'])
@login_required
@check_scope(scope_required="delete")
def delete_movie():
    request_body=request.get_json()
    validate_request_body('delete_movie',request_body)
    query=f"call delete_movie_data(@id:='{request_body['id']}')"
    print(query)
    execute_query(query)
    return create_success_response()
