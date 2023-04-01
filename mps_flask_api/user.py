from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash,abort ,jsonify, redirect, url_for, request,g
from database import define_db, get_db


def session_init():
    if 'session' not in globals():
        session = {}
        return session
    else:
        return globals()['session']

session = session_init()

def read_all():
    db = define_db().cursor(dictionary=True)
    db.execute(
        'SELECT * FROM users')
    users = db.fetchall()
    return jsonify(users)


def create(user):
    # It is using only a html form to create an user

    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        print(f"{user_name} + {password}" )
        g.db = define_db()
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
                session['user_id'] = user['id']
                session['user_name'] = user['username']
            except:
                error = f"Usuário {user_name} já registrado."
                print(error)
            else:
                return redirect(url_for("/api.routes_web_page_index"))
            

def read_one(user_id):
    try:
        db = define_db().cursor(dictionary=True)
        db.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,))
        user = db.fetchone()
    except Exception as e:
        print(e)
        abort(
            404, f"Error: {e}"
        )
    if user:
        return user

def update(user_id, user):
    user_name = user.get("user_name", "")
    user_password = user.get("user_password", "")
    error = None
    userDB = read_one(user_id)

    print(userDB)

    if str(userDB['id']) != user_id:
        error = "Different IDs"
    
    if error is not None:
        abort(
            404, f"{error}"
        )
    else:
        try:
            db = define_db()
            db.cursor().execute(
            'UPDATE users SET username = %s, password = %s '
            ' WHERE id = %s',
            (user_name, generate_password_hash(user_password), user_id)
            )
            db.commit()
        except Exception as e:
            print(e)
        
            
        return user



def delete(user_id):
    event = read_one(user_id)
    db = define_db()
    try:
        db.cursor().execute('DELETE FROM users WHERE id = %s', (user_id,))
        db.commit()
    except Exception as e:
        print(e)

    return event
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        db = define_db().cursor(dictionary=True)
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

