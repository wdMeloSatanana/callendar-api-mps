from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash,abort, make_response,jsonify, redirect, url_for, request,g
import database
import json 

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

USER = {
    "1000": {
        "user_name": "Caio Rolando da Rocha",
        "user_id": "1000",
        "timestamp": get_timestamp(),
    },
    "2000": {
        "user_name": "Jucimar Maia da Silva Jr",
        "user_id": "2000",
        "timestamp": get_timestamp(),
    },
    "3000": {
        "user_name": "Cthonem Martins",
        "user_id": "3000",
        "timestamp": get_timestamp(),
    }
}

session = USER['1000']


def read_all():
    return jsonify(list(USER.values()))


def create(user):
    
 
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        print(f"{user_name} + {password}" )
        g.db = database.define_db()
        db = g.db
        error = None 

        if error is None:
            try:
                db.cursor(dictionary=True).execute(
                    "INSERT INTO users (username, password) VALUES(%s,%s)",
                    (user_name, generate_password_hash(password)),
                )
                db.commit()
                print("Success")
            except:
                error = f"Usuário {user_name} já registrado."
                print(error)
            else:
                return redirect(url_for("/api.routes_web_page_index"))
            

def read_one(user_id):
    if user_id in USER:
        return USER[user_id]
    else:
        abort(
            404, f"Person with ID {user_id} not found"
        )


def update(user_id, user):
    if user_id in USER:
        USER[user_id]["user_name"] = user.get("user_name", USER[user_id]["user_name"])
        USER[user_id]["timestamp"] = get_timestamp()
        return USER[user_id]
    else:
        abort(
            404,
            f"Person with ID {user_id} not found"
        )


def delete(user_id):
    if user_id in USER:
        del USER[user_id]
        return make_response(
            f"{user_id} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Person with ID {user_id} not found"
        )


def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        db = database.define_db().cursor(dictionary=True)
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = %s ', (username,)
        )
        user = db.fetchone()
        
        print(f'Trying to log in as {username } + {password}')
        if user is None:
            error = 'Nome de usuário incorreto.'
        elif not check_password_hash(user['password'], password):
            error = 'Senha incorreta.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            
            return redirect(url_for("/api.routes_web_page_index"))

        flash(error)


def logout():
    session.clear()
    return redirect(url_for('/api.routes_web_page_index'))

