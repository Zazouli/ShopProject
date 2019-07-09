from shopGMT import appshop,bcrypt,db
from flask import render_template, flash,request, redirect, url_for, make_response
from shopGMT.formshop import RegistrationForm, Login
from shopGMT.models import User, Shops, ShopLiked, ShopDisLiked
from flask_login import login_user,current_user,logout_user
from geopy.distance import geodesic
from _datetime import datetime,timedelta


@appshop.route('/', methods=['GET', 'POST'])
@appshop.route('/home', methods=['GET', 'POST'])
@appshop.route('/login', methods=['GET', 'POST'])
def homeshop():
    if current_user.is_authenticated:
        return redirect('landingpage')
    form = Login()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('landingpage'))
        else:
            flash('Your password or email are wrong !!', 'danger')
    return render_template('homeshop.html', titre='Home', form=form)


@appshop.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('landingpage')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash('12345').decode('UTF-8')
        user= User(email=form.email.data,password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your Accout has been created you can now login', 'success')
        return redirect(url_for('homeshop'))
    return render_template('registershop.html', title='Registration', form=form)

@appshop.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homeshop'))

@appshop.route('/landingpage',methods=['POST','GET'])
def landingpage():
    if current_user.is_authenticated:
        return render_template('pageShop.html')
    else:
        return redirect(url_for('homeshop'))
@appshop.route('/Nearby')
def Nearby():
    if current_user.is_authenticated:
        alt=request.args["alt"]
        long=request.args["long"]
        id=[]
        shoplike=ShopLiked.query.all()
        shopdislike=ShopDisLiked.query.all()
        for like in shoplike:
            id.append(like)
        for dislike in shopdislike:
            id.append(dislike)
            deldisl(dislike)
        Shop=Shops.query.all()
        for ids in id:
            for shops in Shop:
                if shops.id == ids.shop_id :
                    Shop.remove(shops)
        me=(alt,long)
        dist=[]
        for shop in Shop:
            place=(shop.shopAlte,shop.shopLong)
            theplace=geodesic(me,place).km
            c=(theplace,shop.id,shop.shopName,shop.shopStats)
            dist.append(c)
        dist.sort()
        return render_template('Nearby.html',alt=alt,long=long,theplace=dist)
    else:
        return redirect(url_for('homeshop'))
@appshop.route('/like/<int:a>')
def like(a):
    if current_user.is_authenticated:
        shoplike=ShopLiked(user_id=current_user.id,shop_id=a)
        shops=Shops.query.filter_by(id=a).first()
        shops.shopStats=1
        db.session.add(shoplike)
        db.session.commit()
        return redirect(url_for('landingpage'))
    else:
        return redirect(url_for('homeshop'))
@appshop.route('/dislike/<int:a>')
def dislike(a):
    if current_user.is_authenticated:
        shopdislike=ShopDisLiked(user_id=current_user.id,shop_id=a)
        shops=Shops.query.filter_by(id=a).first()
        shops.shopStats=2
        db.session.add(shopdislike)
        db.session.commit()
        return redirect(url_for('landingpage'))
    else:
        return redirect(url_for('homeshop'))
@appshop.route('/likedshop')
def likedshop():
    if current_user.is_authenticated:
        shoplike=ShopLiked.query.filter_by(user_id=current_user.id)
        shop=[]
        for shopli in shoplike:
            shop.append(Shops.query.filter_by(id=shopli.shop_id).first())
        return render_template('likedshop.html',theplace=shop)
    else:
        return redirect(url_for('homeshop'))
@appshop.route('/remove/<int:a>')
def remove(a):
    if current_user.is_authenticated:
        shoplike=ShopLiked.query.filter_by(user_id=current_user.id).filter_by(shop_id=a).first()
        db.session.delete(shoplike)
        db.session.commit()
        return redirect(url_for('likedshop'))
    else:
        return redirect(url_for('homeshop'))

def deldisl(dislike):
    disliketime = dislike.time_disl + timedelta(hours=0, minutes=2, seconds=0)
    compare = datetime.now()
    if disliketime < compare :
        db.session.delete(dislike)
        db.session.commit()
    return
