import calendar
from flask_appbuilder import ModelView 
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_babel import lazy_gettext as _


from app import db, appbuilder
from .models import ContactGroup, Gender, Contact, Department, Gender, StudentDetails


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ['name', 'personal_celphone', 'birthday', 'contact_group.name']

    base_order = ('name', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    delete_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)

def pretty_year(value):
    return str(value.year)

class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            'group' : 'month_year',
            'formatter': pretty_month_year,
            'series': [(aggregate_count, 'group')]
        },
        {
            'group': 'year',
            'formatter': pretty_year,
            'series': [(aggregate_count, 'group')]
        }
    ]


class StudentModelView(ModelView):
    datamodel = SQLAInterface(StudentDetails)
    list_columns = ['name', 'birthday', 'department.name']
    base_order = ('name', 'asc')
    show_fieldsets = [('Student Personal Details', {'fields': ['name', 'gender', 'department', 'address', 'birthday', 'personal_phone']})]
    add_fieldsets = [('Student Personal Details', {'fields': ['name', 'gender', 'department', 'address', 'birthday', 'personal_phone']})]
    edit_fieldsets = [('Student Personal Details', {'fields': ['name', 'gender', 'department', 'address', 'birthday', 'personal_phone']})]


class DepartmentModelView(ModelView):
    datamodel = SQLAInterface(Department)
    related_views = [StudentModelView]


db.create_all()
fill_gender()
appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Contacts", category_icon='fa-envelope')
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_view(ContactTimeChartView, "Contacts Birth Chart", icon="fa-dashboard", category="Contacts")


appbuilder.add_view(DepartmentModelView, "List Department", icon="fa-folder-open-o", category="Students", category_icon='fa-envelope')
appbuilder.add_view(StudentModelView, "List Student", icon="fa-envelope", category="Students")







