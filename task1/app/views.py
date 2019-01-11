from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, SimpleFormView, BaseView, expose, has_access
from app import appbuilder, db
from flask_appbuilder.models.group import aggregate_count
from flask_babel import lazy_gettext as _
from .models import EmployeeTable
from .forms import MyForm
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()

class MyView(BaseView):
    route_base = "/api/v1"
    @expose('/empdata', methods=['GET'])
    def employee_data(self):
        emp_data = session.query(EmployeeTable).filter().all()
        print('emp_data',emp_data)
        return json.dumps(emp_data)
                  
appbuilder.add_view_no_menu(MyView())

