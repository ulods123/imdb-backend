from flask import Flask



app=Flask(__name__)

@app.route('/health',methods=['GET'])
def health():
    return "Yo I am running!!!"


if __name__=="__main__":
    app.run()