from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def serialise(self):
        return {
            'id': self.id,
            'created_on': self.created_on,
            'updated_on': self.updated_on,
        }


class Food(Base):
    __tablename__ = 'food'
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)  # TODO: change to two floats
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, location, description):
        super(Food, self).__init__()
        self.name = name
        self.location = location
        self.description = description

    def serialise(self):
        return {**(super(Food, self).serialise()), **{
            'name': self.name,
            'location': self.location,
            'description': self.description,
        }}
