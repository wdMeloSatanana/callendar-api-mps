from flask import (
    Blueprint,render_template, current_app, g)
import user, database, calendario


def web_page_index():
    print(current_app)
    print(user.session)
    posts = database.get_db()
    user.session['data-visualizada'], user.session['mes-visualizado'], user.session['mes-objeto'] = calendario.data_util()
    return render_template('base.html', posts=posts, session=user.session)

def web_page_create():
    return render_template("events/create.html")

def web_page_update_event():
    return render_template("events/update.html")

def web_page_login():
    return render_template("login.html")

def web_page_register():
    return render_template("register.html")

def web_page_update_user():
    return render_template("register.html")
