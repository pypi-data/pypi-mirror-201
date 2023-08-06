from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                LOGIN_NAME)
from genesys.app.blueprints.task.utils import create_task_file, delete_task_file
from genesys.app.services import svn_service, queue_store
from genesys.app.utils import config_helpers
import os
from configparser import ConfigParser, NoSectionError, NoOptionError
from genesys.app import config

task = Blueprint('task', __name__)
api = Api(task)

def update_svn_acl(data, project_name):
    if data['person'][LOGIN_NAME] != '':
        task = data['task']
        main_file_name = data['main_file_name']
        base_svn_directory = data['base_svn_directory']
        acl_parser = ConfigParser()
        svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name.replace(' ', '_').lower(), 'conf/authz')

        splited_file_map_folder_url = base_svn_directory.split(':', 1)
        base_file_directory = f"{splited_file_map_folder_url[0]}{splited_file_map_folder_url[1]}"
        file_name = os.path.basename(base_file_directory).rsplit('.', 1)[0]

        for_entity = task["task_type"]["for_entity"]
        if for_entity.lower() == "asset":
            base_map_svn_directory = os.path.join(os.path.dirname(base_svn_directory), 'maps', main_file_name)
        else:
            base_map_svn_directory = os.path.join(os.path.dirname(base_svn_directory), 'maps', file_name)

        config_helpers.load_config(svn_authz_path, acl_parser)
        svn_service.svn_update_acl(
            base_svn_directory=base_svn_directory,
            acl_parser=acl_parser,
            person=data['person'][LOGIN_NAME],
            permission=data['permission']
        )
        svn_service.svn_update_acl(
            base_svn_directory=base_map_svn_directory,
            acl_parser=acl_parser,
            person=data['person'][LOGIN_NAME],
            permission=data['permission']
        )
        if data['permission'] == 'rw':
            for dependency_base_svn_directory in data['dependencies']:
                dependency_base_map_svn_directory = os.path.join(os.path.dirname(dependency_base_svn_directory), 'maps', main_file_name)
                svn_service.svn_update_acl(
                    base_svn_directory=dependency_base_svn_directory,
                    acl_parser=acl_parser,
                    person=data['person'][LOGIN_NAME],
                    permission='r'
                )
                svn_service.svn_update_acl(
                    base_svn_directory=dependency_base_map_svn_directory,
                    acl_parser=acl_parser,
                    person=data['person'][LOGIN_NAME],
                    permission='r'
                )
        
        elif data['permission'] == 'none':
            for dependency_base_svn_directory in data['dependencies']:
                dependency_base_map_svn_directory = os.path.join(os.path.dirname(dependency_base_svn_directory), 'maps', main_file_name)
                svn_service.svn_update_acl(
                    base_svn_directory=dependency_base_svn_directory,
                    acl_parser=acl_parser,
                    person=data['person'][LOGIN_NAME],
                    permission='d'
                )
                svn_service.svn_update_acl(
                    base_svn_directory=dependency_base_map_svn_directory,
                    acl_parser=acl_parser,
                    person=data['person'][LOGIN_NAME],
                    permission='d'
                )
        config_helpers.write_config(svn_authz_path, acl_parser)


class Task(Resource):
    def post(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                create_task_file,
                args=(data['task'], project_name, base_file_directory, data['base_svn_directory'], data['main_file_name']),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            create_task_file(
                            task=data['task'],
                            project_name=project_name,
                            base_file_directory=base_file_directory,
                            base_svn_directory=data['base_svn_directory'],
                            main_file_name=data['main_file_name']
                                )
            return jsonify(message=f'task created')

    def delete(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                delete_task_file,
                args=(project_name, base_file_directory),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            delete_task_file(project_name, base_file_directory, task_type=data['task_type'])
            return jsonify(message=f'task deleted')


class Task_File_Access_Control(Resource):
    def put(self, project_name):
        data = request.get_json()
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                update_svn_acl,
                args=(data, project_name),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            update_svn_acl(data, project_name)
            project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
            return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)


api.add_resource(Task, '/task/<string:project_name>')
api.add_resource(Task_File_Access_Control, '/task_acl/<string:project_name>')