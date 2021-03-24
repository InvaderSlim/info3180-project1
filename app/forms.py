# from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class NewPropertyForm(FlaskForm):
    """Add New Property form"""

    title = StringField(
        'Property Title',
        [DataRequired()]
    )
    description = TextAreaField(
        'Description',
        [DataRequired()]
    )
    rooms = IntegerField(
        'No. of Rooms',
        [
            DataRequired()
        ]
    )
    baths = StringField(
        'No. of Bathrooms',
        [
            DataRequired()
        ]
    )
    price = StringField(
        'Price',
        [
            DataRequired()
        ]
    )
    property_type = SelectField(
        u'Property Type', 
        choices=[('House','House'), ('Apartment','Apartment')]
    )
    location = StringField(
        'Location',
        [DataRequired()]
    )

    photo = FileField(
        'Photo',
        [FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images of format .png or .jpg')]
    )
    submit = SubmitField('Submit')