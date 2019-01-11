import calendar
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from app import db, appbuilder
from .models import City, Gender, Emp
from flask_appbuilder import AppBuilder, expose, ModelView, has_access
from app import appbuilder
from flask import redirect, url_for
from flask import Flask, render_template, request
import sqlite3 as sql
import sqlite3


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Emp)

    list_columns = ['name', 'birthday', 'city.name']

    base_order = ('name', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'city', 'address', 'birthday', 'personal_phone'], 'expanded': False}),
    ]

class GroupModelView(ModelView):
    datamodel = SQLAInterface(City)
    related_views = [ContactModelView]

db.create_all()
fill_gender()
appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Emps", category_icon='fa-envelope')
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Emps")


