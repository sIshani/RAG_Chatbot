from flask import Flask, render_template, request
from backend import response                    #to handle chat responses


app = Flask(__name__)                           #creates an instance of flask class to run the web application

@app.route('/')
def index():                                    #handles requests to root url
    return render_template('index.html')        #renders the html template

#def chat():
    #user_url = request.form.get('url')
    #message = request.form.get('msg')
    #if not user_url or not message:
        #return jsonify({"answer": "Please provide both a URL and a message."})
    #answer = response(user_url, message) 
    #return jsonify({"answer": answer})


@app.route('/chat', methods=['GET', 'POST'])     #defines a route to the chat url that accepts both requests
def chat():
    message = request.form['msg']               #retrieves the message parameter from the incoming data
    return response(message)                    #calls the response function from the backend file



if __name__ == '__main__':
    app.run()                                  #starts the flask server and checks if script is running directly