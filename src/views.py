from flask import render_template, Blueprint, request, redirect
from src.models import Models


views = Blueprint('views', __name__)
models = Models()


@views.route('/proj/<string:project_id>', methods=['GET', 'POST'])
def proj(project_id):
    """
    /proj endpoint which is used for current project pointer change and redirects to home
    :param project_id: new project id
    :return: home redirection
    """
    models.update_current_project_id(project_id)
    return redirect('/')


@views.route('/', methods=['GET', 'POST'])
def index():
    """
    Default endpoint
    :return: home template
    """
    return render_template('home.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects())


@views.route('/requirements', methods=['GET', 'POST'])
def requirements():
    """
    Requirements endpoint
    :return: requirements template
    """
    all_reqs = list(models.mongo.find(({"$and":
                                        [{'requirement_id': {'$exists': 'true'}},
                                         {'parent_project': models.get_current_project_id()['title'].lower()}]})))
    return render_template('requirements.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects(),
                           requirements=all_reqs)


@views.route('/bugs', methods=['GET', 'POST'])
def bugs():
    """
    Bugs endpoint
    :return: ugs template
    """
    return render_template('bugs.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects())


@views.route('/tc', methods=['GET', 'POST'])
def tc():
    """
    Test cases endpoint
    :return: tc template
    """
    return render_template('tc.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects())


@views.route('/req/<string:req_id>', methods=['GET', 'POST'])
def req(req_id):
    """
    req endpoint
    :param req_id: requirement id in format REQ-{req_number}
    :return: req template
    """
    found_req = list(models.mongo.find({"object_id": req_id}))
    if found_req:
        return render_template('req.html',
                               req=found_req[0],
                               current_project=models.get_current_project_id(),
                               projects=models.get_all_projects())
    else:
        return redirect('/requirements')


@views.route('/create', methods=['GET', 'POST'])
def create():
    """
    Create endpoint
    :return: create template
    """
    if request.method == 'POST':
        post_form = request.form
        models.create(post_form)
    return render_template('create.html',
                           current_project=models.get_current_project_id(),
                           projects=models.get_all_projects())
