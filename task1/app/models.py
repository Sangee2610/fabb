import datetime
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from flask_appbuilder import ModelView, SimpleFormView, BaseView, expose, has_access

mindate = datetime.date(datetime.MINYEAR, 1, 1)

class EmployeeTable(Model):

    __tablename__ = "employee_table"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    designation = Column(String(564))
    job_location = Column(String(564))  

    def __init__(self, **kwargs):
        super(EmployeeTable, self).__init__(**kwargs)

    def __repr__(self):
        return self.name
        


  





