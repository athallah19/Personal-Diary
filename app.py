from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connect_string = 'mongodb+srv://test:sparta@cluster0.5qv8bta.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connect_string)
db = client.dbsparta2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary2.find({}, {'_id': False}))
    return jsonify({'articles': articles})
    
@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary2.insert_one(doc)
    return jsonify({'message' : 'data tersimpan!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)