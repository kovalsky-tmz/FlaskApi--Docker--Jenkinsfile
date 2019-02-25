# FlaskApi-Jenkins-Docker
 Docker image : kowal20x7/flaskapi<br>
 Existing user: <b> Login:</b> test, <b>Password: </b> test

<h2>Api</h2>

<h4>Login</h4>
POST   /login    - to get jwt token, -d {'username':'','password':''}<br>
Bearer Token Required
<h4>Posts</h4>
GET    /posts<br>
POST   /posts    - -d {'title','content'}<br>
PUT    /post/{id}<br>
DELETE /post/{id}<br>
GET    /post/{id}<br>
<h4>Users</h4>
GET    /users<br>
POST   /users    - to add new user, -d {'username':'','password':''}<br>
PUT    /user/{id}<br>
DELETE /user/{id}<br>
GET    /user/{id}<br>
