from datetime import datetime
from imp import reload
from flask import render_template, url_for, flash, redirect, request, abort
from formbuilder import app, db, bcrypt
from formbuilder.forms import LoginForm, RegistrationForm, ViewForm
from formbuilder.models import Formtitles, Questions, Replies, User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/home", methods=['GET', 'POST'])
def home():
    t = Formtitles.query.filter_by(uid=current_user.id)
    return render_template('home.html',t=t)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('create.html')

@app.route("/store", methods=['POST'])
def store():
    a=request.form
    l1,l2,l3=[],[],[]
    qu = Questions.query.filter_by(uid=current_user.id).order_by(Questions.id.desc())
    if(qu.first()):
        k = qu.first().id   
    else:
        k=0
    b,c,d,e=0,0,0,0
    print(a)
    for i in a:
        if(i[0]=="q"):
            b+=1
        else:
            if(i[0]=="d"):
                c+=1
                l1.append(i)
            if(i[0]=="t"):
                d+=1
                l2.append(i)
            if(i[0]=="c"):
                e+=1
                l3.append(i)
    for i in range(1,b+1):
        s = "q"+str(i)
        q = request.form.get(s)
        question = Questions(id=k+1,name=s,uid=current_user.id,data=q)
        db.session.add(question)
        db.session.commit()
    for j in range(c):
        s = "dr"+str(j)
        ques = Questions.query.filter_by(id=k+1,name="q"+l1[j][2]).first()
        try:
            r = Replies(id=k+1,qid=ques.sno,uid=current_user.id,data="date")
            db.session.add(r)
            db.session.commit() 
        except:
            r = Replies(id=k+1,qid=ques.sno-1,uid=current_user.id,data="date")
            db.session.add(r)
            db.session.commit() 
    for l in range(d):
        s = "tr"+str(l)
        ques = Questions.query.filter_by(id=k+1,name="q"+l2[l][2]).first()
        try:
            t = Replies(id=k+1,qid=ques.sno,uid=current_user.id,data="textfield")
            db.session.add(t)
            db.session.commit() 
        except:
            t = Replies(id=k+1,qid=ques.sno-1,uid=current_user.id,data="textfield")
            db.session.add(t)
            db.session.commit() 
    for n in range(e):
        s = "cr"+str(n)
        ques = Questions.query.filter_by(id=k+1,name="q"+l3[n][2]).first()
        try:
            cb = Replies(id=k+1,qid=ques.sno,uid=current_user.id,data="checkbox")
            db.session.add(cb)
            db.session.commit() 
        except:
            cb = Replies(id=k+1,qid=ques.sno-1,uid=current_user.id,data="checkbox")
            db.session.add(cb)
            db.session.commit() 
    td = request.form.get("hl")
    f = Formtitles(id=k+1,title=td,uid=current_user.id)
    db.session.add(f)
    db.session.commit()
    
    return redirect(url_for('home'))

@app.route("/view/<int:fid>", methods=['GET','POST'])
def view(fid):
    form = ViewForm()
    t = Formtitles.query.filter_by(uid=current_user.id,id=fid).first()
    q = Questions.query.filter_by(uid=current_user.id,id=fid)
    r = Replies.query.filter_by(uid=current_user.id,id=fid)
    return render_template('view.html',q=q,r=r,form=form,t=t)