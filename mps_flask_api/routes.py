from flask import (
    Blueprint,render_template, current_app, g)
import user


def web_page_index():
    print(current_app)
    print(user.session)
    return render_template('base.html', session=user.session)

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
