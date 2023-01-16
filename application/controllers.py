from flask import request,redirect,render_template,session, url_for, request
from flask import current_app as app
from application.models import *
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    msg="You Need To Login First!!!"
    return render_template("login.html",f=True, msg=msg)

@app.route("/",methods=['GET', 'POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        uname=request.form["uname"]
        pa=request.form["pass"]
        print(uname,pa)
        f=True
        b=Bcrypt()
        if uname!="" and pa!="":
            users=Users.query.all()
            for user in users:
                if uname==user.username and b.check_password_hash(user.password,pa):
                    f=False
                    login_user(user)
                    return redirect(url_for("feed",uid=user.id))
        if f:
            msg="Invalid Credentials"
            return render_template("login.html",f=f,msg=msg)

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        uname=request.form["uname"]
        pa=request.form["pass"]
        cpa=request.form["cpass"]
        pic=request.files["image"]
        filename=secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if pa!=cpa or not pic or not uname or not pa or not cpa:
            return render_template("register.html",f=True,msg="Enter The Fields Properly!")
        if uname!="" and pa!="":
            users=Users.query.all()
            for user in users:
                if uname==user.username:
                    return render_template("register.html",f=True,msg="Username Already Exists!")
            b=Bcrypt()
            pa=b.generate_password_hash(pa).decode('utf-8')
            USER=Users(username=uname,password=pa,name=filename)
            db.session.add(USER)
            db.session.commit()
            return redirect("/")
        else:
            return render_template("register.html",f=True)

@app.route("/userfeed/<int:uid>",methods=["GET","POST"])
@login_required
def feed(uid):
    if request.method=="GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        following = [follower.id for follower in user.following]
        posts = db.session.query(Blogs).order_by(Blogs.created_at.desc()).filter(Blogs.uid.in_(following))
        return render_template("feed.html",posts=posts,user=user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/blog/<int:uid>",methods=['GET','POST'])
@login_required
def blog(uid):
    if request.method=="GET":
        user=db.session.query(Users).filter(Users.id == uid).first()
        return render_template("blog.html",user=user)
    if request.method=="POST":
        user=db.session.query(Users).filter(Users.id==uid).first()
        title=request.form["title"]
        caption=request.form["caption"]
        pic=request.files["image"]
        if not title or not caption or not pic:
            return render_template("blog.html",f=True)
        filename=secure_filename(pic.filename + "_" + str(user.id))
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blog=Blogs(title=title,caption=caption,name=filename,uid=user.id)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("feed",uid=uid))

@app.route('/profile/<int:uid>')
@login_required
def profile(uid):
    if request.method=="GET":
        user=db.session.query(Users).filter(Users.id==uid).first()
        return render_template("profile.html",user=user)

@app.route('/search/<int:uid>')
@login_required
def search(uid):
    if request.method=="GET":
        users=Users.query.all()
        user=db.session.query(Users).filter(Users.id == uid).first()
        return render_template("search.html",user=user,users=users)

@app.route('/follow/<int:uid>/<int:fid>')
@login_required
def follow(uid, fid, methods=['POST']):
    user=db.session.query(Users).filter(Users.id==uid).first()
    followee=db.session.query(Users).filter(Users.id==fid).first()
    user.following.append(followee)
    db.session.commit()
    return redirect(url_for("search",uid=uid))

@app.route('/unfollow/<int:uid>/<int:fid>')
@login_required
def unfollow(uid, fid, methods=['POST']):
    user = db.session.query(Users).filter(Users.id == uid).first()
    followee = db.session.query(Users).filter(Users.id == fid).first()
    user.following.remove(followee)
    db.session.commit()
    return redirect(url_for("search", uid=uid))

@app.route('/followers/<int:uid>')
@login_required
def followers(uid):
    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        return render_template("followers.html", user=user, users=user.followers)

@app.route('/following/<int:uid>')
@login_required
def following(uid):
    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        return render_template("following.html", user=user, users=user.following)

@app.route('/following/follow/<int:uid>/<int:fid>')
@login_required
def following_follow(uid, fid, methods=['POST']):
    user = db.session.query(Users).filter(Users.id == uid).first()
    followee = db.session.query(Users).filter(Users.id == fid).first()
    user.following.append(followee)
    db.session.commit()
    return redirect(url_for("following", uid=uid))

@app.route('/following/unfollow/<int:uid>/<int:fid>')
@login_required
def following_unfollow(uid, fid, methods=['POST']):
    user = db.session.query(Users).filter(Users.id == uid).first()
    followee = db.session.query(Users).filter(Users.id == fid).first()
    user.following.remove(followee)
    db.session.commit()
    return redirect(url_for("following", uid=uid))

@app.route('/followers/follow/<int:uid>/<int:fid>')
@login_required
def followers_follow(uid, fid, methods=['POST']):
    user = db.session.query(Users).filter(Users.id == uid).first()
    followee = db.session.query(Users).filter(Users.id == fid).first()
    user.following.append(followee)
    db.session.commit()
    return redirect(url_for("followers", uid=uid))

@app.route('/followers/unfollow/<int:uid>/<int:fid>')
@login_required
def followers_unfollow(uid, fid, methods=['POST']):
    user = db.session.query(Users).filter(Users.id == uid).first()
    followee = db.session.query(Users).filter(Users.id == fid).first()
    user.following.remove(followee)
    db.session.commit()
    return redirect(url_for("followers", uid=uid))

@app.route('/<int:uid>/profile/<int:fid>')
@login_required
def otherprofile(uid, fid):
    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        other = db.session.query(Users).filter(Users.id == fid).first()
        return render_template("other_profile.html", user=user,other=other)

@app.route('/delete/<int:uid>/<int:pid>')
@login_required
def delete(uid, pid):
    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        post = db.session.query(Blogs).filter(Blogs.id == pid).first()
        user.blogs.remove(post)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("profile",uid=uid))


@app.route('/edit/<int:uid>/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit(uid,pid):
    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        post = db.session.query(Blogs).filter(Blogs.id == pid).first()
        return render_template("edit.html",user=user,post=post)
    if request.method == "POST":
        user = db.session.query(Users).filter(Users.id == uid).first()
        post = db.session.query(Blogs).filter(Blogs.id == pid).first()
        title = request.form["title"]
        caption = request.form["caption"]
        pic = request.files["image"]
        if not title or not caption or not pic:
            return render_template("edit.html", f=True)
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        post.title=title
        post.caption=caption
        post.name=filename
        db.session.commit()
        return redirect(url_for("profile", uid=uid))


@app.route('/pedit/<int:uid>', methods=['GET', 'POST'])
@login_required
def pedit(uid):
    if request.method == "GET":
        user = db.session.query(Users).filter(Users.id == uid).first()
        return render_template("pedit.html", user=user)
    if request.method == "POST":
        user = db.session.query(Users).filter(Users.id == uid).first()
        desc = request.form["desc"]
        pic = request.files["image"]
        if not desc or not pic:
            return render_template("pedit.html",user=user, f=True)
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user.desc = desc
        user.name = filename
        db.session.commit()
        return redirect(url_for("profile", uid=uid))

@app.route('/<int:uid>/post/<int:pid>',methods=['GET','POST'])
@login_required
def post(uid,pid):
    user=db.session.query(Users).filter(Users.id == uid).first()
    post=db.session.query(Blogs).filter(Blogs.id == pid).first()
    if request.method == "GET":
        return render_template("post.html",post=post,user=user,f=False)
    if request.method == "POST":
        user = db.session.query(Users).filter(Users.id == uid).first()
        post = db.session.query(Blogs).filter(Blogs.id == pid).first()
        text = request.form["comment"]
        if not text:
            return render_template("post.html", post=post, user=user, f=True)
        comment = comments(uid=uid, pid=pid, text=text)
        db.session.add(comment)
        db.session.commit()
        return render_template("post.html", post=post, user=user, f=False)

@app.route('/<int:uid>/like/<int:pid>/<string:s>')
@login_required
def like(uid, pid, s, methods=['POST']):
    like=db.session.query(likes).filter(likes.uid==uid,likes.pid==pid).first()
    if like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = likes(uid=uid, pid=pid)
        db.session.add(like)
        db.session.commit()
    if s=="0":
        return redirect(url_for("post", uid=uid, pid=pid))
    elif s=="-1":
        return redirect(url_for("feed", uid=uid))
    elif s=="-2":
        return redirect(url_for("profile", uid=uid))
    else:
        return redirect(url_for("otherprofile", uid=uid, fid=int(s)))



@app.route('/<int:uid>/dlike/<int:pid>')
@login_required
def dlike(uid, pid):
    user=db.session.query(Users).filter(Users.id==uid).first()
    post=db.session.query(Blogs).filter(Blogs.id==pid).first()
    return render_template("likers.html",user=user,post=post)

@app.route('/<int:uid>/dcomment/<int:cid>')
@login_required
def delcomment(uid, cid, methods=['POST']):
    comment=db.session.query(comments).filter(comments.id==cid).first()
    pid=comment.pid
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("post", uid=uid, pid=pid))