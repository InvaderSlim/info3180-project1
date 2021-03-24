"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
from .forms import NewPropertyForm
from .models import Properties


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

@app.route('/property', methods=["GET", "POST"])
def property():
    """Add new property form"""
    root_dir = os.getcwd()
    form = NewPropertyForm()

        # Validate file upload on submit
    if request.method == 'POST' and form.validate_on_submit():

        img = form.photo.data
        filename = secure_filename(img.filename)
        
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['ALLOWED_EXTENSIONS']:
                flash('Invalid format, try again')


        title=request.form['title']
        description=request.form['description']
        rooms=request.form['rooms']
        baths=request.form['baths']
        price=request.form['price']
        property_type=request.form['property_type']
        location=request.form['location']

        # title = form.title.data
        # description = form.description.data
        # rooms = form.rooms.data
        # baths = form.baths.data
        # price = form.price.data
        # property_type = form.property_type.data
        # location = form.location.data

        properties = Properties(
            title,
            description,
            rooms,
            baths,
            price,
            property_type,
            location,
            filename
        )

        db.session.add(properties)
        db.session.commit()    
        
        img.save(os.path.join( 
            root_dir, app.config['UPLOAD_FOLDER'], filename
        ))

        
        flash('Property Listed', 'success')
        return redirect(url_for('properties'))
    
    
    if request.method == 'GET':
        return render_template('property.html', form=form)
    flash("Error in form",'danger')
    return render_template('property.html', form=form, template="form-template")

@app.route('/properties/')
def properties():
    """Display all properties"""
    properties = Properties.query.all()
    return render_template('properties.html', properties=properties)

@app.route("/view_property/<propertyid>")
def view_property(propertyid):
    property_ = Properties.query.get(int(propertyid))
    return render_template('view_property.html', property_=property_)
    


@app.route("/get_image/<filename>")
def get_image(filename):
    root_dir=os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
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
