from . import db

class Properties(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    rooms = db.Column(db.String(3))
    baths = db.Column(db.String(3))
    price = db.Column(db.String(20))
    property_type = db.Column(db.String(11))
    location = db.Column(db.String(255))
    photo = db.Column(db.String(80), unique=True)



    def __init__(self, title, description, rooms, baths, price, property_type, location, photo):
        self.title = title
        self.description = description
        self.rooms = rooms
        self.baths = baths
        self.price = price
        self.property_type = property_type
        self.location = location
        self.photo = photo



    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.title)
