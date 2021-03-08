import pymysql
import json



connection=pymysql.connect("sql6.freemysqlhosting.net", "sql6397037", "P6mwKRcq4A",
						   "sql6397037")

def execute_query(query):
	print("Connection created")
	row={}
	cursor=connection.cursor(pymysql.cursors.DictCursor)
	try:
		# print(query)
		cursor.execute(query)
		#print(cursor.rowcount,"Row Count")
		if cursor.rowcount == 1:
			row=cursor.fetchone()
		else:
			row=cursor.fetchall()
		#print(row,"Row")
		return {"Success": True, "Row": row}
	except Exception as e:
		print(e)
		raise Exception("Procedure failed with query" + query)
	finally:
		connection.commit()
		cursor.close()
		#connection.close()

with open('imdb.json','r') as f:
	data=json.loads(f.read())

query="select * from genre";
genre_result=execute_query(query)["Row"]
print(genre_result)

query="select * from movie";
movie_result=execute_query(query)["Row"]

movie_genre_dict=[]	
for row in movie_result:
	for subrow in data :
		if row["name"]==subrow["name"] and row["director"]==subrow["director"]:
			abc=subrow['genre'] 
			print(abc)
			for genre in abc:
				print(genre)
				tmp={}
				genre_id=[gen["id"] for gen in genre_result if gen["name"]==genre.strip()]
				tmp['movie_id']=row["id"]
				tmp['genre_id']=genre_id[0]
				movie_genre_dict.append(tmp)
print(movie_genre_dict)

for row in movie_genre_dict:
	query=f"insert into movie_genre_mapping (movie_id,genre_id) values ({row['movie_id']},{row['genre_id']})"
	execute_query(query)
'''
genre=set()
for row in data:
	genre.update([gen.strip() for gen in row["genre"] ])
print(genre)

for row in genre:
	query=f"insert into genre (name) values ('{row.strip()}')"
	print(query)
	execute_query(query)
'''
