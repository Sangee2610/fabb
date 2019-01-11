from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm


class MyForm(DynamicForm):
    field1 = StringField(('Name'),
        description=('Your field number one!'),
        validators = [DataRequired()], widget=BS3TextFieldWidget())
    field2 = StringField(('Designation'),
        description=('Your field number two!'), widget=BS3TextFieldWidget())
    field3 = StringField(('Company'),
        description=('Your field number three!'),widget=BS3TextFieldWidget())
    field4 = StringField(('Job Location'),
        description=('Your field number four!'), widget=BS3TextFieldWidget())
