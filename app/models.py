from app import db

class Bucketlist(db.Model):
    # This class represents the bucketlist table & inherits from the 'db.Model'

    __tablename__ = 'bucketlists' #Should always be plural

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        # Initialize with name

        self.name = name
    def save(self):
        db.session.add(self)

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)
