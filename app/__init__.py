import ZODB,ZODB.FileStorage,BTrees.OOBTree
import transaction
import sys
import zc
import time
import os

from flask import Flask
app=Flask(__name__)
app.config.from_object('config')
from app.models import User
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
# from config import basedir

lm=LoginManager()
lm.init_app(app)
lm.login_view='login'
print lm

basedir = os.path.abspath(os.path.dirname(__file__))
oid=OpenID(app,os.path.join(basedir,'tmp'))
print oid

dbOpen=0
root=None

try:
    storage=ZODB.FileStorage.FileStorage('c:/dev/PycharmProjects/USIHelpSystem/helpdesk.fs')
    dbOpen=1
except zc.lockfile.LockError:
    print('**** ZODB connection is already open!')
except:
    print("Unexpected error:", sys.exc_info()[0])

if dbOpen:
    db = ZODB.DB(storage)
    connection = db.open()
    root=connection.root()

    for record in root['tickets']:
        ticket=root['tickets'][record]
        print ticket.requestor

    # root['users']={}
    # root['users']['1']=User('1','Walker','walker.west@gmail.com')
    # root['users']['2']=User('2','Ben','bdbrown4@eagles.usi.edu')
    # transaction.commit()

    for record in root['users']:
        user = root['users'][record]
        print user

from app import views,models
