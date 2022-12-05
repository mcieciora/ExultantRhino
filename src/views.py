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
    chart_data = {}
    active_bugs = list(models.mongo.find({'$and': [{'object_type': 'bug'},
                                                   {'parent_project': models.get_current_project_id()['title']}]}))
    number_of_test_cases = len(list(models.mongo.find({'$and': [{'object_type': 'testcase'},
                                                   {'parent_project': models.get_current_project_id()['title']}]})))
    not_covered_requirements = [key for key, value in models.get_dependencies('requirement', extended_key=True).items()
                                if len(value) == 0]
    number_of_requirements = len(list(models.mongo.find((
        {'$and': [{'object_type': 'requirement'},
                  {'parent_project': models.get_current_project_id()['title']}]}))))
    total_release_coverage = list(models.mongo.find(
        {'$and': [{'object_type': 'release'},
                  {'parent_project': models.get_current_project_id()['title']}]}))
    if total_release_coverage:
        chart_data['title'] = total_release_coverage[-1]['title']
        chart_data['values'] = list(total_release_coverage[-1]['results'].values())
        chart_data['keys'] = list(total_release_coverage[-1]['results'].keys())
    return render_template('home.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           active_bugs=active_bugs,
                           not_covered_requirements=not_covered_requirements,
                           chart_data=chart_data,
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
    if object_type == 'releases':
        all_releases = list(models.mongo.find({'$and': [{'object_type': 'release'},
                                                        {'parent_project': models.get_current_project_id()['title']}]}))
        return render_template('view_objects.html',
                               current_project=models.get_current_project_id(),
                               projects=models.get_all_projects(),
                               all_objects=all_releases)
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


@views.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    upload endpoint
    :return: status code
    """
    all_requirements = models.get_test_case_requirements_dependencies()
    content = request.json
    results = {'fail': 0, 'pass': 0, 'not_run': 0}
    try:
        release_name = content['release_name']
        project_name = content['project_name']
        reqs = content['reqs']
    except KeyError:
        return 'wrong request: release_name, project_name and reqs are required keys', 400
    for req_id, test_cases in reqs.items():
        try:
            for test_case, result in test_cases.items():
                all_requirements[req_id][test_case] = result
                results[result] += 1
        except KeyError:
            continue
    models.mongo.insert({'object_type': 'release', 'title': release_name, 'parent_project': project_name,
                         'object_id': models.get_next_id(), 'requirements': all_requirements, 'results': results})
    return 'success', 200
