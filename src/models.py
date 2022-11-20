from src.pymongo_db import MongoDb


class Models:
    """
    Model class is used for database models creation and validation of inputs.
    """

    def __init__(self):
        self.mongo = MongoDb('test_db', 'test_col')
        all_projects = self.get_all_projects()
        if all_projects:
            self.project_pointer = all_projects[0]['project_id']
        else:
            self.mongo.insert({'project_id': 'PROJ-0', 'title': 'Template', 'object_type': 'project'})
            self.project_pointer = 'PROJ-0'
        self.models = {'project': {'object_id': 'project_id', 'object_id_prefix': 'PROJ'},
                       'bug': {'object_id': 'bug_id', 'object_id_prefix': 'BUG'},
                       'requirement': {'object_id': 'requirement_id', 'object_id_prefix': 'REQ'},
                       'test_case': {'object_id': 'tc_id', 'object_id_prefix': 'TC'}}

    def update_current_project_id(self, _id):
        """
        update_current_project_id changes value of current project pointer
        :param _id: new pointer id
        :return: None
        """
        self.project_pointer = _id

    def get_current_project_id(self):
        """
        get_current_project_id look for project object in database with current project pointer as a key
        :return: current project object
        """
        return list(self.mongo.find({'project_id': self.project_pointer}))[0]

    def get_all_projects(self):
        """
        get_all_projects lists all projects in database
        :return: list of all projects in database
        """
        return list(self.mongo.find({'object_type': 'project'}))

    def get_next_id(self, object_type, model):
        """
        get_next_id looks for latest object in database with specified object type and gets last id number and returns
        id string
        :param object_type: object type from list [requirement, project, bug, test_case]
        :param model: object data model
        :return: full id string in format: {prefix}-{id_number}
        """
        all_objects_with_type = list(self.mongo.find({'object_type': object_type}))
        if all_objects_with_type:
            id_number = all_objects_with_type[-1][model['object_id']].split('-')[1]
            next_id_number = int(id_number) + 1
        else:
            next_id_number = 0
        return f"{model['object_id_prefix']}-{next_id_number}"

    def create(self, input_dict):
        """
        create function takes input dict with post form values which are later transformed into model object, that is
        inserted into database
        :param input_dict: data dict
        :return: None
        """
        model = self.models[input_dict['object_type']]
        new_object = {'title': input_dict['title'], 'description': input_dict['description'],
                      'object_type': input_dict['object_type'],
                      model['object_id']: self.get_next_id(input_dict['object_type'], model)}
        if 'parent_project' in input_dict.keys() and input_dict['object_type'] != 'project':
            new_object['parent_project'] = input_dict['parent_project']
        if 'parent' in input_dict.keys():
            new_object['parent'] = input_dict['parent']
        self.mongo.insert(new_object)
