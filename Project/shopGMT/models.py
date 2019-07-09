from _datetime import datetime
from shopGMT import appshop, db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(130), unique=False, nullable=False)
    liked = db.relationship('ShopLiked', backref='Like', lazy=True)
    disliked = db.relationship('ShopDisLiked', backref='disLike', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.password}')"


class Shops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopName = db.Column(db.String(100), nullable=False)
    shopStats = db.Column(db.Integer, nullable=False, default=0)
    shopLong = db.Column(db.String(50), nullable=False)
    shopAlte = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.shopName}','{self.shopStats}','{self.shopLong}','{self.shopAlte}')"


class ShopLiked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)


class ShopDisLiked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    time_disl = db.Column(db.DateTime, default=datetime.utcnow)
