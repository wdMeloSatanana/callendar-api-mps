from datetime import datetime
from flask import abort,jsonify, request, flash, redirect, url_for
import user
from database import define_db, get_db



def read_all():
    all_posts = jsonify(get_db())
    return all_posts


def create(event):
    event_title = event.get("event_title", "")
    event_body = event.get("event_body", "")
    event_timestamp = event.get("timestamp", "")
    event_author_id = event.get("author_id", "")

    db = define_db()
    try:
        db.cursor(dictionary=True).execute(
            'INSERT INTO event (title, body, author_id, time)'
            ' VALUES (%s, %s, %s, %s)',
            (event_title, event_body, event_author_id, event_timestamp),
        )
        db.commit()

        return 201
    except Exception as e:
        print(e)
        abort(
            406,
            f"Event with title {event_title} failed",
        )




def create_form():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        timestamp  = request.form['time']
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M')
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:00")
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = define_db()
            db.cursor(dictionary=True).execute(
                'INSERT INTO event (title, body, author_id, time)'
                ' VALUES (%s, %s, %s, %s)',
                (title, body, user.session['user_id'], timestamp),
            )
            db.commit()
            return redirect(url_for('/api.routes_web_page_index'))




def read_one(event_id):
    db = define_db().cursor(dictionary=True)
    error = None
    try:
        event = db.execute(
            'SELECT * FROM event WHERE id = %s ', (event_id,)
        )
        event = db.fetchone()
    except Exception as e:
        print(e)
        error = e
        abort(
            404, f"Error: {error}"
        )

    if event:
        return event


def update(event_id, event):
    event_title = event.get("event_title", "")
    event_body = event.get("event_body", "")
    event_timestamp = event.get("timestamp", "")
    event_author_id = event.get("author_id", "")
    error = None
    eventDB = read_one( event_id)


    if str(eventDB['author_id']) != event_author_id:
        error = "Different ID"
    
    if error is not None:
        abort(
            404, f"{error}"
        )
    else:
        try:
            db = define_db()
            db.cursor().execute(
            'UPDATE event SET title = %s, body = %s, time = %s '
            ' WHERE id = %s',
            (event_title, event_body, event_timestamp, event_id)
            )
            db.commit()
        except Exception as e:
            print(e)
        
            
        return event




def delete(event_id):
    event = read_one(event_id)
    db = define_db()
    try:
        db.cursor().execute('DELETE FROM event WHERE id = %s', (event_id,))
        db.commit()
    except Exception as e:
        print(e)

    return event