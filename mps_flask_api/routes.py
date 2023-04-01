from flask import (
    Blueprint,render_template, current_app, g, redirect, url_for)
import user, database, calendario
from database import get_db


def web_page_index():
    print(current_app)
    print(user.session)
    posts = get_db()
    print(posts)
    user.session['data-visualizada'], user.session['mes-visualizado'], user.session['mes-objeto'] = calendario.data_util()
    return render_template('home.html', posts=posts, session=user.session, month=user.session['mes-objeto'])

def web_page_create():
    if 'user_id' not in user.session:
        return redirect(url_for("/api.routes_web_page_index"))
    return render_template("events/create.html")

def web_page_update_event():
    return render_template("events/update.html")

def web_page_login():
    return render_template("login.html")

def web_page_register():
    return render_template("register.html")

def web_page_update_user():
    return render_template("register.html")
