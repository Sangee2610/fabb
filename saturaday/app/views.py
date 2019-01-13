from flask_appbuilder import AppBuilder, expose, BaseView, has_access
from app import appbuilder
from flask import redirect, url_for
from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)
# Create connection
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

class MyView(BaseView):
    default_view = 'home'    
    @expose('/home/')
    @has_access
    def home(self): 
        return render_template('home.html')

    @expose('/enternew/')
    @has_access
    def new_student(self):
        return self.render_template('student.html')
    
    @expose('/search/')
    @has_access
    def search(self):
        return self.render_template('search.html')
	
    @expose('/addrec/',methods = ['POST', 'GET'])
    @has_access
    def addrec(self):
        if request.method == 'POST':
            try:
                i = request.form['i']
                nm = request.form['nm']
                addr = request.form['add']
                city = request.form['city']
                pin = request.form['pin']
                #engine.execute('CREATE TABLE "EX1" ('
                #                 'id INTEGER NOT NULL,'
                #                 'name VARCHAR, '
                #                 'addr VARCHAR, '
                #                 'city VARCHAR, '
                #                 'pin VARCHAR, '
                #                 'PRIMARY KEY (id));')
                engine.execute('INSERT INTO "EX1" '
                                '(id, name,addr,city,pin) '
                                'VALUES (?,?,?,?,?)',(i,nm,addr,city,pin) )
                engine.commit()
                msg = "Record successfully added"
            except:
                con.rollback()
                msg = "error in insert operation"   
            finally:
                return render_template("result.html")#,msg = msg)
                con.close()

    
    
	
    @expose('/list/',methods = ['POST', 'GET'])
    @has_access
    def list(self):
        if request.method == 'POST':
            #con = sql.connect("database.db")
            con = engine.connect()
            choice = request.form['choice']
            #con.row_factory = engine.Row 
            #cur = con.cursor()
            if choice=='bangalore':
                 #cur.execute("select * from employee where city='bangalore'")
                 res=con.execute('SELECT * FROM '
                        '"EX1"')
                 rows = res.fetchall();
                 return render_template("list.html",rows = rows)
                
            elif choice=='chennai':
                 #cur.execute("select * from employee where city='chennai'")
                 res=con.execute('SELECT * FROM '
                        '"EX1"')
                 rows = res.fetchall();
                 return render_template("list.html",rows = rows)
                
            else:
                 #cur.execute("select * from employee")
                 res=con.execute('SELECT * FROM '
                        '"EX1"')
                 rows = res.fetchall();
                 return render_template("list.html",rows = rows)

    @expose('/empdata', methods=['GET'])
    def employee_data(self):
        emp_data = session.query(MyView).filter().all()
        print('emp_data',emp_data)
        return json.dumps(emp_data)

appbuilder.add_view(MyView, "Home", category='My View')

