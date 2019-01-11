from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, BaseView, expose
from app import appbuilder, db

from flask import Flask, jsonify 
from flask import abort 
from flask import make_response 
from flask import request 
from flask import url_for 

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good python tutorial',
        'done': False
    }
] 

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


class ApiView(BaseView):
    route_base = "/api/v1"
    default_view = "index"

    @expose("/index")
    def index(self):
        #return jsonify({'tasks': map(make_public_task, tasks)}) 
        print(repr(request.args))
        print(repr(request.method))
        print(repr(request.headers))
        return jsonify(tasks)

    @expose("/get_token")
    def get_token(self):
        print(repr(request.headers))
        return jsonify({'res': True})

    @expose("/get_resource")
    def get_resource(self):
        return jsonify({'res': False})

    @expose("/del_resource")
    def del_resource(self):
        return jsonify({'res': False})

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()

appbuilder.add_view_no_menu(ApiView())
