class TicketExample:
    def __init__(self,requestor,date,problem):
        self.requestor=requestor
        self.date=date
        self.problem=problem

class Item():

    def __init__(self,item):
        self.item=item
        self.models=[]

    def addModel(self,model):
        self.models.append(model)

class User():

    def __init__(self,id,nickname,email):
        self.id=id
        self.nickname=nickname
        self.email=email

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def is_authenticated(self):
        return True
