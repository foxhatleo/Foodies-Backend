from flask_sqlalchemy import SQLAlchemy, event

db = SQLAlchemy()


class Base(db.Model):
    """
    Base is the root model of all other models in the app. It has an id field, a created_on and a updated_on field. Base
    itself should not be used directly unless defining another model, and it does not correspond to a table in the
    database.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                           server_onupdate=db.func.current_timestamp())

    @classmethod
    def date_format(cls, d):
        """Format a date as "Dec 2, 2015". """
        return "{dt:%b} {dt.day}, {dt:%y}".format(dt=d)

    @classmethod
    def time_format(cls, t):
        """Format a time as "3:15 am". """
        return "{tm:%I}:{tm:%M} {tm:%p}".format(tm=t)

    @classmethod
    def datetime_format(cls, d):
        """Format a datetime as "Dec 2, 2015 3:15 am". """
        return "{} {}".format(cls.date_format(d), cls.time_format(d))

    def serialise(self):
        """Serialise the object into a Python dictionary."""
        co = self.datetime_format(self.created_on)
        uo = self.datetime_format(self.updated_on)
        return {
            "id": self.id,
            "created_on": co,
            "updated_on": uo,
        }


class Food(Base):
    """
    Food is the model for a free food event.
    """

    __tablename__ = "food"
    title = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    location_detail = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    tags = db.Column(db.String, nullable=False)
    image = db.Column(db.Text, nullable=True, default="")

    def __init__(self, title, location, location_detail, description, date, tags, start_time, end_time, image=""):
        super(Food, self).__init__()
        self.title = title
        self.location = location
        self.location_detail = location_detail
        self.description = description
        self.date = date
        self.tags = tags
        self.start_time = start_time
        self.end_time = end_time
        self.image = image

    def serialise(self):
        """Serialise the object into a Python dictionary."""
        st = self.time_format(self.start_time)
        et = self.time_format(self.end_time)
        da = self.date_format(self.date)
        ta = self.tags.split("\r")
        return {**(super(Food, self).serialise()), **{
            "title": self.title,
            "location": self.location,
            "location_detail": self.location_detail,
            "description": self.description,
            "start_time": st,
            "end_time": et,
            "date": da,
            "tags": ta,
            "image": self.image,
        }}


@event.listens_for(Food.__table__, "after_create")
def insert_initial_values(*_args, **_kwargs):
    """Insert initial values for the database here."""
    db.session.commit()
