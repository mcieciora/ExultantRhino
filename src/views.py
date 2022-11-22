from flask import render_template, Blueprint, request, redirect
from src.models import Models


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
    Requirements endpoint
    :return: view_objects template
    """
    all_objects = list(models.mongo.find(({"$and": [{'object_id': {'$exists': 'true'}},
                                                    {'object_type': object_type},
                                                    {'parent_project': models.get_current_project_id()['title']}]})))
    return render_template('view_objects.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           all_objects=all_objects)


@views.route('/create', methods=['GET', 'POST'])
def create():
    """
    Create endpoint
    :return: create template
    """
    if request.method == 'POST':
        post_form = dict(request.form)
        post_form['parent_project'] = models.get_current_project_id()['title']
        models.create(post_form)
    return render_template('create.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects())


@views.route('/view/<string:object_id>', methods=['GET', 'POST'])
def view(object_id):
    """
    view endpoint
    :param object_id: object id in format OBJ-{object_number}
    :return: view template
    """
    found_object = list(models.mongo.find({"object_id": object_id}))
    if found_object:
        return render_template('view.html',
                               object=found_object[0],
                               current_project=models.get_current_project_id(),
                               projects=models.get_all_projects())
    else:
        return redirect('/')
