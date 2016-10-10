from app import oid,lm,app,root
#from app import app
from flask import render_template,flash,redirect,session,url_for,request,g
from flask.ext.login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,ItemForm,DelForm
from .models import User,Item
import uuid
import transaction

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    form=ItemForm();
    delForm=DelForm();
    user=g.user
    if form.validate_on_submit():
        newItem = Item(id=str(uuid.uuid1()),item=form.item.data)
        print("myUUID is "+newItem.id)
        root['items'][newItem.id]=newItem
        root._p_changed=1
        transaction.commit()
        # print("Adding item return ... "+myVal)
        flash('New item added!')
        return redirect(url_for('index'))
    if delForm.validate_on_submit():
        print("deleting "+delForm.id.data)
        del root['items'][delForm.id.data]
        root._p_changed=1
        transaction.commit()
        flash('Item deleted!')
        return redirect(url_for('index'))
    itemsOfInterest=root['items']

    # [
    #     {
    #         'item': 'Lawn Mower',
    #         'models': [ 'Honda','Black & Decker' ]
    #     },
    #     {
    #         'item': 'Weed Eater',
    #         'models': [ 'Torro','Echo' ]
    #     }
    # ]

    # user={'nickname':'Ben'}
    return render_template('index.html',
                           title='USI Help System',
                           user=user,
                           itemsOfInterest=itemsOfInterest,
                           form=form,
                           delForm=delForm)

@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpenID="%s",remember_me=%s' %
        #       (form.openid.data, str(form.remember_me.data)))
        # return redirect('/index')
        session['remember_me']=form.remember_me.data
        return oid.try_login(form.openid.data,ask_for=['nickname','email'])
    return render_template('login.html',
                           title="Sign In",
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    # user = root['users'][record]
    # print user.nickname
    print "User "+id+" is logging on!"
    return root['users'].get(id)

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    # user = User.query.filter_by(email=resp.email).first()
    user=None
    for record in root['users']:
        myUser = root['users'][record]
        if(myUser.email==resp.email):
            print("The target e-mail is "+resp.email)
            user=myUser

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))