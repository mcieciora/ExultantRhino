from flask import render_template, Blueprint, request, redirect
from src.models import Models, ProjectExistsError


views = Blueprint('views', __name__)
models = Models()


@views.route('/', methods=['GET', 'POST'])
def index():
    """
    Default endpoint
    :return: home template
    """
    return render_template('home.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects())


@views.route('/proj/<string:project_id>', methods=['GET', 'POST'])
def proj(project_id):
    """
    /proj endpoint which is used for current project pointer change and redirects to home
    :param project_id: new project id
    :return: home redirection
    """
    models.update_current_project_id(project_id)
    return redirect('/')


@views.route('/view_objects/<string:object_type>', methods=['GET', 'POST'])
def view_objects(object_type):
    """
    View objects endpoint
    :return: view_objects template
    """
    all_objects = list(models.mongo.find(({"$and": [{'object_id': {'$exists': 'true'}},
                                                    {'object_type': object_type},
                                                    {'parent_project': models.get_current_project_id()['title']}]})))
    dependencies = {}
    for obj in all_objects:
        _id = obj['object_id']
        dependencies[_id] = list(models.mongo.find({'parent': {'$regex': _id}}))
    return render_template('view_objects.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           all_objects=all_objects,
                           dependencies=dependencies)


@views.route('/create', methods=['GET', 'POST'])
def create():
    """
    Create endpoint
    :return: create template
    """
    if request.method == 'POST':
        post_form = dict(request.form)
        post_form['parent_project'] = models.get_current_project_id()['title']
        try:
            models.create(post_form)
        except ProjectExistsError:
            pass
    return render_template('create.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           objects=models.mongo.find({}))


@views.route('/edit/<string:object_id>', methods=['GET', 'POST'])
def edit(object_id):
    """
    view endpoint
    :param object_id: object id in format OBJ-{object_number}
    :return: view template
    """
    found_object = list(models.mongo.find({"object_id": object_id}))
    if request.method == 'POST':
        post_form = dict(request.form)
        models.edit(object_id, post_form)
    elif found_object:
        return render_template('edit.html',
                               object=found_object[0],
                               current_project=models.get_current_project_id(),
                               projects=models.get_all_projects(),
                               objects=models.mongo.find({}))
    return redirect('/')


@views.route('/delete/<string:object_id>', methods=['GET', 'POST'])
def delete(object_id):
    models.delete(object_id)
    return redirect('/')
