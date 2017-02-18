"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/add-file', methods=['POST', 'GET'])
def add_file():
    if not session.get('logged_in'):
        abort(401)

    file_folder = app.config['UPLOAD_FOLDER']

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_folder, filename))

        flash('File Saved')
        return redirect(url_for('home'))

    return render_template('add_file.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in')
            return redirect(url_for('add_file'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/file_listing')
def file_listing():
    if not session.get('logged_in'):
        abort(401)

    rootdir = os.getcwd()
    path = '/app/static/uploads'
    print rootdir
    jpgs = list()
    uploads = list()
    for subdir, dirs, files in os.walk(rootdir + path):
        for file in files:
            if file != '.gitkeep':
                if file.endswith('.jpg') or file.endswith('.jpeg'):
                    jpgs.append(file)
                else:
                    uploads.append(file)

    return render_template('file_listings.html', path=path, jpgs=jpgs, uploads=uploads)

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.route('/<file_name>.mp4')
def send_mp4_file(file_name):
    """Send your static text file."""
    file_dot_mp4 = file_name + '.mp4'
    return app.send_static_file(file_dot_mp4)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
