# http://www.ibm.com/developerworks/aix/library/au-zodb/
# http://www.zodb.org/en/latest/tutorial.html
# pip install ZODB
#
# https://www.jetbrains.com/pycharm/
#
# Python 2.7.11
#
# Python O.O.:
# http://www.tutorialspoint.com/python/python_classes_objects.htm
#
# PyInstaller:
# https://github.com/pyinstaller/pyinstaller
#
# Flask
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

from flask import Flask

class Ticket:
    def __init__(self,requestor,date,problem):
        self.requestor=requestor
        self.date=date
        self.problem=problem

#root['tickets']={}
#root['tickets']['tick1']=Ticket("Walker","2016-10-04","need help with Python")
#root['tickets']['tick2']=Ticket("USIHelpSystem","2016-10-03","need help with ODK")
#transaction.commit()

#from app import app
# app.run(debug=True)

def import_on_first_request(environ,start_response):
    from app import app
    app.debug=True
    return app(environ,start_response)

from werkzeug import run_simple
run_simple('localhost',5000,import_on_first_request)
