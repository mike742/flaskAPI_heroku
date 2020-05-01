from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# mySQL config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test'

# postreSQL config
__env__ = 'PROD' #'DEV' PROD

if __env__ == 'DEV':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://inqtandoehzlzt:616376d92f787001c0f4817091d6b952a59f20e7a4c62fb815ca07d38d563bac@ec2-54-152-175-141.compute-1.amazonaws.com:5432/d5m4n1rdv7e29i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Jokes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstSentence = db.Column(db.String(256))
    secondSentence = db.Column(db.String(256))

    def __init__(self, firstSentence, secondSentence):
        self.firstSentence = firstSentence
        self.secondSentence = secondSentence


class JokeSchema(ma.Schema):
    class Meta:
        fields = ("id", "firstSentence", "secondSentence")


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getAll', methods=['GET'])
def getAll():
    all_jokes = Jokes.query.all()
    return jsonify(jokes_schema.dump(all_jokes))


@app.route('/get/<id>/', methods=['GET'])
def get(id):
    joke = Jokes.query.get(id)
    return joke_schema.jsonify(joke)


@app.route('/add', methods=['POST'])
def add():
    content = request.get_json(force=True)
    firstSentence = content['firstSentence']
    secondSentence = content['secondSentence']

    new_joke = Jokes(firstSentence, secondSentence)
    db.session.add(new_joke)
    db.session.commit()

    return joke_schema.jsonify(new_joke)


@app.route('/update/<id>/', methods=['PUT'])
def update(id):
    joke = Jokes.query.get(id)
    
    content = request.get_json(force=True)
    joke.firstSentence = content['firstSentence']
    joke.secondSentence = content['secondSentence']
    db.session.commit()

    return joke_schema.jsonify(joke)


@app.route('/delete/<id>/', methods=['DELETE'])
def delete(id):
    joke = Jokes.query.get(id)
    db.session.delete(joke)
    db.session.commit()

    return joke_schema.jsonify(joke)


if __name__ == "__main__":
    app.run()

