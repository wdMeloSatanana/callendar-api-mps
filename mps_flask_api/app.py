from flask import render_template, request, Flask, send_from_directory  # Remove: import Flask
import connexion
import user
import yaml
from flask_swagger_ui import get_swaggerui_blueprint

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml" )


 
@app.route("/")
def home():
    return render_template("home.html")
 
@app.route('/static/<path: path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/create", methods=['POST'])
def create_user():
    if request.method == 'POST': 
        username = request.form['username']
        user_id = request.form['user_id']
        if username and user_id:
            userDic = {"username": username, "user_id": user_id}
            user.create(userDic)

@app.route("/<string:_id>/update", methods=['PUT'])
def update_user():
    user.update()

@app.route("/<string:_id>/delete", methods=['DELETE'])
def delete_user():
    user.delete()


@app.route("/listAll", methods=['GET'])
def listAllUsers():
    user.read_all()

@app.route("/listOneUser/<string:_id>", methods=['GET'])
def listOneUser(id):
    user.read_one()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
