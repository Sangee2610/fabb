from flask_appbuilder import AppBuilder, expose, BaseView, has_access
from app import appbuilder
from flask import redirect, url_for
from flask import Flask, render_template, request
import sqlite3 as sql
import sqlite3

#conn=sqlite3.connect('database.db')
#conn.execute('DROP TABLE employee;')
#conn.execute('CREATE TABLE employee (id TEXT,name TEXT, addr TEXT, city TEXT, pin TEXT)')

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
                with sql.connect("database.db") as con:
                   cur = con.cursor()
                   cur.execute("INSERT INTO employee (id,name,addr,city,pin) VALUES (?,?,?,?,?)",(i,nm,addr,city,pin) )
                   con.commit()
                   msg = "Record successfully added"
            except:
                con.rollback()
                msg = "error in insert operation"   
            finally:
                return render_template("result.html",msg = msg)
                con.close()

    
    
	
    @expose('/list/',methods = ['POST', 'GET'])
    @has_access
    def list(self):
        if request.method == 'POST':
            con = sql.connect("database.db")
            choice = request.form['choice']
            con.row_factory = sql.Row 
            cur = con.cursor()
            if choice=='bangalore':
                 cur.execute("select * from employee where city='bangalore'")
                 rows = cur.fetchall();
                 return render_template("list.html",rows = rows)
                
            elif choice=='chennai':
                 cur.execute("select * from employee where city='chennai'")
                 rows = cur.fetchall();
                 return render_template("list.html",rows = rows)
                
            else:
                 cur.execute("select * from employee")
                 rows = cur.fetchall();
                 return render_template("list.html",rows = rows)

appbuilder.add_view(MyView, "Home", category='My View')

