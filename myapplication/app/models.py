#myapplication
import datetime
from flask import Markup, url_for
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app import db
from flask_appbuilder.models.mixins import AuditMixin, BaseMixin, FileColumn, ImageColumn
from flask_appbuilder.filemanager import ImageManager, get_file_original_name
from flask_appbuilder import Model



class PersonGroup(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(50), unique = True, nullable=False)
    address = Column(String(264))
    phone1 = Column(String(20))
    phone2 = Column(String(20))
    taxid = Column(Integer)
    notes = Column(Text())

    def __repr__(self):
        return self.name


class Person(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address =  Column(String(564))
    date_of_joining = Column(Date)
    photo = Column(ImageColumn(thumbnail_size=(30, 30, True), size=(300, 300, True)))
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    personal_email = Column(String(64))
    notes = Column(Text())
    business_function = Column(String(64))
    business_phone = Column(String(20))
    business_celphone = Column(String(20))
    business_email = Column(String(64))
    person_group_id = Column(Integer, ForeignKey('person_group.id'))
    person_group = relationship("PersonGroup")

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) +\
                          '" class="thumbnail"><img src="' + im.get_url(self.photo) +\
                          '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="'+ url_for('PersonModelView.show',pk=str(self.id)) +\
                          '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) +\
                          '" class="thumbnail"><img src="' + im.get_url_thumbnail(self.photo) +\
                          '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="'+ url_for('PersonModelView.show',pk=str(self.id)) +\
                          '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

class Project(AuditMixin, Model):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)


class ProjectFiles(Model):
    __tablename__ = "project_files"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship("Project")
    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="' + url_for('ProjectFilesModelView.download', filename=str(self.file)) + '">Download</a>')

    def file_name(self):
        return get_file_original_name(str(self.file))      
        
          
