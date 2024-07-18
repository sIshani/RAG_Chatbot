from flask import Flask, render_template, request
from file import response                    #to handle chat responses
from dotenv import load_dotenv   


load_dotenv()                                   #loads environment variables from env file into environment
app = Flask(__name__)  

@app.route('/')
def index():                                    #handles requests to root url
    return render_template('index.html')        #renders the html template

@app.route('/chat', methods=['GET', 'POST']) 
def chat():
    message=request.form['msg']             #retrieves message parameter from incoming data
    user_url = request.form["url"] 

    return response(message, user_url)                   #calls the response function from the file 

if __name__== '__main__':
    app.run()                                  #starts the flask server and checks if script is running directly