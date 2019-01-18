#myapplication
from .models import Person, PersonGroup
from flask_appbuilder.views import ModelView, BaseView,CompactCRUDMixin
from app.models import Project, ProjectFiles
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.widgets import ListThumbnail
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models import Project, ProjectFiles


from app import app, db, appbuilder


class PersonModelView(ModelView):
    datamodel = SQLAInterface(Person, db.session)

    list_title = 'List Contacts'
    show_title = 'Show Contact'
    add_title = 'Add Contact'
    edit_title = 'Edit Contact'

    label_columns = {'person_group_id': 'Group', 'photo_img': 'Photo', 'photo_img_thumbnail': 'Photo'}
    list_columns = ['photo_img_thumbnail', 'name', 'business_celphone','business_function', 'date_of_joining', 'person_group']

    show_fieldsets = [
        ('Summary', {'fields': ['photo_img', 'name', 'address', 'person_group']}),
        ('Personal Info',
         {'fields': ['date_of_joining', 'personal_celphone', 'personal_email'], 'expanded': False}),
        ('Professional Info',
         {'fields': ['business_function', 'business_celphone', 'business_email'], 'expanded': False}),
        ('Extra', {'fields': ['notes'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'photo', 'address', 'person_group']}),
        ('Personal Info',
         {'fields': ['date_of_joining',  'personal_celphone', 'personal_email'], 'expanded': False}),
        ('Professional Info',
         {'fields': ['business_function', 'business_celphone', 'business_email'], 'expanded': False}),
        ('Extra', {'fields': ['notes'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'photo', 'address', 'person_group']}),
        ('Personal Info',
         {'fields': ['date_of_joining', 'personal_celphone', 'personal_email'], 'expanded': False}),
        ('Professional Info',
         {'fields': ['business_function', 'business_celphone', 'business_email'], 'expanded': False}),
        ('Extra', {'fields': ['notes'], 'expanded': False}),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(PersonGroup, db.session)
    related_views = [PersonModelView]

    label_columns = {'phone': 'Phone (1)', 'taxid': 'Tax ID'}
    list_columns = ['name', 'notes']


class PersonChartView(GroupByChartView):
    datamodel = SQLAInterface(Person)
    chart_title = 'Grouped Persons'
    label_columns = PersonModelView.label_columns
    chart_type = 'BarChart'

    definitions = [
        {
            'group': 'person_group',
            'series': [(aggregate_count,'person_group')]
        }
    ]

class ProjectFilesModelView(ModelView):
    datamodel = SQLAInterface(ProjectFiles)

    label_columns = {'file_name': 'File Name', 'download': 'Download'}
    add_columns = ['file', 'description','project']
    edit_columns = ['file', 'description','project']
    list_columns = ['file_name', 'download']
    show_columns = ['file_name', 'download']


class ProjectModelView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(Project)
    related_views = [ProjectFilesModelView]

    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'

    add_columns = ['name']
    edit_columns = ['name']
    list_columns = ['name', 'created_by', 'created_on', 'changed_by', 'changed_on']
    show_fieldsets = [
        ('Info', {'fields': ['name']}),
        ('Audit', {'fields': ['created_by', 'created_on', 'changed_by', 'changed_on'], 'expanded': False})
    ]

db.create_all()
appbuilder.add_view(GroupModelView(), "List Team", icon="fa-folder-open-o", category="Team")
appbuilder.add_view(PersonModelView(), "Team Members", icon="fa-envelope", category="Team")
appbuilder.add_view(PersonChartView(), "Team View", icon="fa-dashboard", category="Team")
appbuilder.add_view(ProjectModelView, "List Projects", icon="fa-table", category="Projects")
appbuilder.add_view_no_menu(ProjectFilesModelView)

