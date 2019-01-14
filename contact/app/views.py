from flask_appbuilder import AppBuilder, expose, BaseView, has_access
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.widgets import FormHorizontalWidget, FormInlineWidget, FormVerticalWidget
from flask_babel import lazy_gettext as _
from app import db, appbuilder
from .models import ContactGroup, Gender, Contact
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import (Blueprint, request, make_response, jsonify)
import requests
import tabulate
import ast

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ['name','contact_group.name']

    base_order = ('name', 'asc')
    show_fieldsets = [('Summary', {'fields': ['name', 'gender', 'contact_group','address', 'personal_phone']})]

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

class MyView(BaseView):
    route_base = "/api/vi"
    @expose('/empdata', methods=['GET','POST'])
    def employee_data(self):
        emp_data = session.query(Contact).filter().all()
        li = []
        for x in emp_data:
             mydict = {'name' : x.name,
		       'address' : x.address}
		   
             li.append(mydict)
        return json.dumps(li)

class GetApi(BaseView):
    route_base = "/api/vi"
    @expose('/getdata', methods=['GET','POST'])
    def get_data(self):
        url = "http://localhost:8080/api/vi/empdata" 
        headers = {
          'cache-control': "no-cache",
          'postman-token': "72c97887-727e-ae9e-36ed-182f725fb6b5"
           }
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text) 
        ult_list = ast.literal_eval(json.dumps(data))
        header = ult_list[0].keys()  
        rows =  [x.values() for x in ult_list]
        return tabulate.tabulate(rows, header)

db.create_all()
fill_gender()
appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Contacts", category_icon='fa-envelope')
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_link("empdata", href='/api/vi/empdata', category='Contacts')
appbuilder.add_link("getdata", href='/api/vi/getdata', category='Contacts')
appbuilder.add_view_no_menu(MyView())
appbuilder.add_view_no_menu(GetApi())



