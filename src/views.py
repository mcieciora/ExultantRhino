from flask import render_template, Blueprint, request, redirect, flash
from src.models import Models


views = Blueprint('views', __name__)
models = Models()


@views.route('/', methods=['GET', 'POST'])
def index():
    """
    Default endpoint
    :return: home template
    """
    active_bugs = list(models.mongo.find({'object_type': 'bug'}))
    number_of_test_cases = len(list(models.mongo.find({'object_type': 'testcase'})))
    not_covered_requirements = [key for key, value in models.get_dependencies('requirement').items() if len(value) == 0]
    number_of_requirements = len(list(models.mongo.find({'object_type': 'requirement'})))
    total_release_coverage = None
    return render_template('home.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           active_bugs=active_bugs,
                           not_covered_requirements=not_covered_requirements,
                           total_release_coverage=total_release_coverage,
                           number_of_test_cases=number_of_test_cases,
                           number_of_requirements=number_of_requirements)


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
    return render_template('view_objects.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           all_objects=models.get_all_objects_of_type(object_type),
                           dependencies=models.get_dependencies(object_type))


@views.route('/create', methods=['GET', 'POST'])
def create():
    """
    Create endpoint
    :return: create template
    """
    if request.method == 'POST':
        post_form = dict(request.form)
        if post_form['object_type'] == 'project':
            post_form['parent_project'] = 'Template'
        else:
            post_form['parent_project'] = models.get_current_project_id()['title']

        models.create(post_form)
        flash(f"{post_form['title']} was successfully created.", category='success')
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
        flash(f"{post_form['title']} was successfully edited.", category='success')
    elif found_object:
        return render_template('edit.html',
                               object=found_object[0],
                               current_project=models.get_current_project_id(),
                               projects=models.get_all_projects(),
                               objects=models.mongo.find({}))
    return redirect('/')


@views.route('/delete/<string:object_id>', methods=['GET', 'POST'])
def delete(object_id):
    """
    delete endpoint
    :param object_id: object id in format OBJ-{object_number}
    :return: home redirection
    """
    models.delete(object_id)
    flash(f"{object_id} was successfully deleted.", category='success')
    return redirect('/')
