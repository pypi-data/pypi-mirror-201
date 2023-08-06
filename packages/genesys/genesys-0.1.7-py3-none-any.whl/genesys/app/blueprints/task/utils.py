import os
from genesys.app.services import svn_service
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, TEMPLATE_FILES_DIR
from genesys.app.utils import config_helpers
from configparser import ConfigParser
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                LOGIN_NAME)
import bpy

def create_task_file(task, project_name, base_file_directory, base_svn_directory, main_file_name):
    "creates file tasks"
    acl_parser = ConfigParser()
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name.replace(' ', '_').lower(), 'conf/authz')
    file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
    file_extension = os.path.basename(base_file_directory).rsplit('.', 1)[1]
    if file_extension == 'blend':
        template_file = os.path.join(TEMPLATE_FILES_DIR,'blender.blend')
    elif file_extension == 'clip':
        template_file = os.path.join(TEMPLATE_FILES_DIR,'clipstudio.clip')
    elif file_extension == 'flp':
        template_file = os.path.join(TEMPLATE_FILES_DIR,'flstudio.flp')
    elif file_extension == 'tif':
        template_file = os.path.join(TEMPLATE_FILES_DIR,'sketchbook.tif')
    else:
        template_file = os.path.join(TEMPLATE_FILES_DIR,'blender.blend')


    config_helpers.load_config(svn_authz_path, acl_parser)

    file_folder_url = os.path.dirname(file_url)
    file_name = os.path.basename(base_file_directory).rsplit('.', 1)[0]

    for_entity = task["task_type"]["for_entity"]
    if for_entity.lower() == "asset":
        collection_name = main_file_name
        file_map_folder_url = os.path.join(file_folder_url, 'maps', main_file_name)
        base_map_svn_directory = os.path.join(os.path.dirname(base_svn_directory), 'maps', main_file_name)
    else:
        collection_name = file_name
        file_map_folder_url = os.path.join(file_folder_url, 'maps', file_name)
        base_map_svn_directory = os.path.join(os.path.dirname(base_svn_directory), 'maps', file_name)
    

    if not svn_service.is_svn_url(file_folder_url):
        svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
    if not svn_service.is_svn_url(file_map_folder_url):
        svn_service.svn_make_dirs(file_map_folder_url, log_message=f'created {file_map_folder_url}')
    if not svn_service.is_svn_url(file_url):
        task_type = task['task_type']['name']
        task_id = task['id']
        entity_id = task['entity_id']
        nagato_file_data = {
            'task_type':task_type,
            'task_id':task_id, 
            'entity_id':entity_id,
            'collection_name': collection_name,
            'scene_name': collection_name,
            'main_file_name': main_file_name,
        }
        if file_extension == 'blend':
            bpy.ops.wm.read_homefile()
            default_collection = bpy.data.collections.get('Collection')
            for obj in default_collection.objects:
                bpy.data.objects.remove(obj, do_unlink=True)  
            bpy.data.collections.remove(default_collection)
            main_collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(main_collection)

            # assets = bpy.data.collections.new("assets")
            # main_collection.children.link(assets)

            bpy.data.scenes['Scene'].name = collection_name
            scene = bpy.data.scenes.get(collection_name)
            scene['nagato_file_data'] = nagato_file_data
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'))
        svn_service.svn_import(path=template_file,
                                    repo_url=file_url,
                                    log_message=f'created {file_url}')
                                   
    create_new_task_acl(base_svn_directory=base_svn_directory, base_map_svn_directory=base_map_svn_directory, acl_parser=acl_parser)
    config_helpers.write_config(svn_authz_path, acl_parser)

def create_new_task_acl(base_svn_directory:str, base_map_svn_directory:str, acl_parser):
    "create svn access entry for task file and set all users to no acces"
    if base_svn_directory in acl_parser:
        pass
    else:
        acl_parser[base_svn_directory] = {
            '@admin':'rw',
            '@super_reader':'r',
            '*':''
        }
        acl_parser[base_map_svn_directory] = {
            '@admin':'rw',
            '@super_reader':'r',
            '*':''
        }

def delete_task_file(project_name, base_file_directory):
    #FIXME  remove acl
    blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
    if svn_service.is_svn_url(blend_file_url):
        svn_service.svn_delete(blend_file_url, log_message=f'created {blend_file_url}')