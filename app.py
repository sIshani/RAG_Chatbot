from flask import Flask, render_template, request
from backend import response


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#def chat():
    #user_url = request.form.get('url')
    #message = request.form.get('msg')
    #if not user_url or not message:
        #return jsonify({"answer": "Please provide both a URL and a message."})
    #answer = response(user_url, message) 
    #return jsonify({"answer": answer})


@app.route('/chat', methods=['GET', 'POST']) 
def chat():
    message = request.form['msg'] 
    return response(message) 



if __name__ == '__main__':
    app.run() 