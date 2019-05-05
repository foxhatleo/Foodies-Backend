from flask_sqlalchemy import SQLAlchemy, event
from datetime import time, date, datetime

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def serialise(self):
        co = self.created_on.strftime("%b ") + str(self.created_on.day) + self.created_on.strftime(", %Y %I:%M %p")
        uo = self.updated_on.strftime("%b ") + str(self.updated_on.day) + self.created_on.strftime(", %Y %I:%M %p")
        return {
            'id': self.id,
            'created_on': co,
            'updated_on': uo,
        }


class Food(Base):
    __tablename__ = 'food'
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
        st = self.start_time.strftime("%I:%M %p")
        et = self.end_time.strftime("%I:%M %p")
        da = self.date.strftime("%b ") + str(self.created_on.day) + self.date.strftime(", %Y")
        ta = self.tags.split("\r")
        return {**(super(Food, self).serialise()), **{
            'title': self.title,
            'location': self.location,
            'location_detail': self.location_detail,
            'description': self.description,
            'start_time': st,
            'end_time': et,
            'date': da,
            'tags': ta,
            'image': self.image,
        }}


@event.listens_for(Food.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Food(title="Hell food",
                        location="Hell",
                        location_detail="Do something bad and you'll be there.",
                        description="Food from hell. Yum!",
                        date=date(2019, 5, 15),
                        start_time=time(12, 0, 0),
                        end_time=time(15, 0, 0),
                        tags="West\rmeals"))
    db.session.add(Food(title="Chinese food",
                        location="Risley",
                        location_detail="Cowcliff",
                        description="Orange chicken!",
                        date=date(2019, 6, 1),
                        start_time=time(15, 0, 0),
                        end_time=time(16, 0, 0),
                        tags="North\rsnacks"))
    db.session.commit()
