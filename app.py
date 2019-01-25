# coding=utf-8
from flask import Flask,jsonify,request,abort,render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

#  musi tu byc bo inaczej nie importuje
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
	get_jwt_identity
)
jwt = JWTManager(app)



# reszta importóww
from models import User,Post
from flask_restful import Api
from serializers import UserSchema,PostSchema
from werkzeug.security import generate_password_hash, \
     check_password_hash

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

#custom error
# @app.errorhandler(404)
# def page_not_found(e):
#     return "error 404"
@app.route('/')
def index():
    # abort(404)
    return jsonify({"msg":"Hello Api"})


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user=User.query.filter_by(username=username).first()
    
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
  
    if user==None or check_password_hash(user.password, password)==False :
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/posts', methods=['GET','POST'])
@jwt_required
def posts():
    if request.method=="GET":
        # posts=Post.query.filter_by(user_id=1)
        posts=Post.query.all()
        result = posts_schema.dump(posts)
        return jsonify(result.data)
    if request.method=="POST":
        current_user = get_jwt_identity()
        id=User.query.filter_by(username=current_user).first().id
        title=request.json.get('title',None)
        content=request.json.get('content',None)
        post=Post(title=title,content=content,user_id=id)
        db.session.add(post)
        db.session.commit()
        return jsonify({"msg":"POST ADDED"})

@app.route('/post/<id>', methods=['GET','DELETE','PUT'])
@jwt_required
def post(id):
    post=Post.query.filter_by(id=id).first()
    result = post_schema.dump(post)
    if request.method=='GET':
        return jsonify(result.data)
    if request.method=="DELETE":
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg":"Post Deleted","post":result.data})
    if request.method=="PUT":
        title=request.json.get('title',None)
        content=request.json.get('content',None)
        post.title=title
        post.content=content
        db.session.commit()
        return jsonify({"msg":"Post Editted","title":title,"content":content})


@app.route('/users', methods=['GET','POST'])
@jwt_required
def users():
    if request.method=="GET":
        # Access the identity of the current user with get_jwt_identity
        users=User.query.all()
        # current_user = get_jwt_identity()
        # return jsonify(logged_in_as=current_user), 200
        result = users_schema.dump(users)
        return jsonify(result.data)
    if request.method=="POST":
        current_user = get_jwt_identity()
        username=request.json.get('username',None)
        if User.query.filter_by(username=username).first() is not None:
            return jsonify({"msg":"This Username is already in use"})
        password=request.json.get('password',None)
        pass_hash = generate_password_hash(password)
        user=User(username=username,password=pass_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg":"USER ADDED"})

@app.route('/user/<id>', methods=['GET','DELETE','PUT'])
@jwt_required
def user(id):
    user=User.query.filter_by(id=id).first()
    result = user_schema.dump(user)
    if request.method=="GET":
        return jsonify(result.data)
    if request.method=="DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg":"User Deleted","user":result.data})
    if request.method=="PUT":
        username=request.json.get('username',None)
        password=request.json.get('password',None)
        user.username=username
        user.password=password
        db.session.commit()
        return jsonify({"msg":"User Editted","username":username,"password":password})

if __name__ == '__main__':
	app.run(host='0.0.0.0')