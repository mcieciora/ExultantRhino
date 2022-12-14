from src.pymongo_db import MongoDb


class Models:
    """
    Model class is used for database models creation and validation of inputs.
    """

    def __init__(self):
        self.mongo = MongoDb('exultant_rhino', 'main_collection')
        all_projects = self.get_all_projects()
        if all_projects:
            self.project_pointer = all_projects[0]['object_id']
        else:
            self.mongo.insert({'object_id': 'OBJ-0', 'title': 'Template', 'object_type': 'project'})
            self.project_pointer = 'OBJ-0'

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
        return self.mongo.find({'object_id': self.project_pointer})[0]

    def get_all_projects(self):
        """
        get_all_projects lists all projects in database
        :return: list of all projects in database
        """
        return self.mongo.find({'object_type': 'project'})

    def get_next_id(self):
        """
        get_next_id looks for latest object in database with specified object type and gets last id number and returns
        id string
        :return: full id string in format: {prefix}-{id_number}
        """
        all_objects_with_type = self.mongo.find({})
        if all_objects_with_type:
            id_number = all_objects_with_type[-1]['object_id'].split('-')[1]
            next_id_number = int(id_number) + 1
        else:
            next_id_number = 0
        return f'OBJ-{next_id_number}'

    def create(self, input_dict):
        """
        create function takes input dict with post form values which are later transformed into model object, that is
        inserted into database
        :param input_dict: data dict
        :return: None
        """
        input_dict['object_id'] = self.get_next_id()
        self.mongo.insert(input_dict)

    def edit(self, object_id, input_dict):
        """
        edit function takes object_id, searches for it in database and replace its values with input_dict
        :param object_id: database object id
        :param input_dict: data dict
        :return: None
        """
        self.mongo.update({'object_id': object_id}, {"$set": input_dict})

    def delete(self, object_id):
        """
        delete function takes object_id, searches for it in database and deletes an object
        :param object_id: database object id
        :return: None
        """
        self.mongo.delete({'object_id': object_id})

    def get_all_objects_of_type(self, object_type):
        """
        get_all_objects_of_type returns list of all object of given type
        :param object_type: object type in bug, project, requirement, testcase
        :return: list of objects
        """
        all_objects = self.mongo.find(({"$and": [{'object_type': object_type},
                                                 {'parent_project': self.get_current_project_id()['title']}]}))
        return all_objects

    def get_dependencies(self, object_type, extended_key=False):
        """
        get_dependencies returns requirements dict with list of all dependent objects
        :param object_type: object type in bug, project, requirement, testcase
        :param extended_key: if true key is extended with requirement title
        :return: dict of requirements id and lists of dependent objects
        """
        dependencies = {}

        for obj in self.get_all_objects_of_type(object_type):
            key = obj['object_id']
            if extended_key:
                key = f"{obj['object_id']}: {obj['title']}"
            dependencies[key] = self.mongo.find({'parent': {'$regex': fr'{obj["object_id"]}:.*'}})
        return dependencies

    def get_test_case_requirements_dependencies(self):
        """
        get_test_case_requirements_dependencies returns dict of requirements ids with dict of dependent test cases with
        not_run value set on default
        :return: dict of dicts
        """
        dependencies = {}
        for obj in self.get_all_objects_of_type('requirement'):
            dependencies[obj['object_id']] = {test_case['object_id']: 'not_run' for test_case in
                                              self.mongo.find({'parent': {'$regex': fr'{obj["object_id"]}:.*'}})}
        return dependencies
