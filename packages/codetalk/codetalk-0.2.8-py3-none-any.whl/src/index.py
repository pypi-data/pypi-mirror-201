import os
import filtration
import time

from config import get_config, set_config

def _find_files(path):
    files = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            files.append(full_path)
        elif os.path.isdir(full_path):
            files.extend(_find_files(full_path))

    return files

def get_files(project_path):
    all_files = _find_files(project_path)
    filtration.update_gitignore(project_path) # TODO use lru_cache

    index_files = {}
    for f in all_files:
        if filtration.should_ignore(f, project_path):
            continue
        try:
            with open(f) as fp:
                content = fp.read()
        except:
            continue
        index_files[f] = content

    return index_files

def insert_project(proj_path, proj_id):
    all_projects = get_config('all_projects') or {}
    all_projects[proj_path] = proj_id
    set_config('all_projects', all_projects)
    set_config('current_project', proj_id)

def get_project(project_path):
    all_projects = get_config('all_projects') or {}
    return all_projects.get(project_path)

def set_project(project_path):
    all_projects = get_config('all_projects') or {}
    try:
        proj_id = all_projects[project_path]
    except KeyError:
        print(f"No index found for project {project_path}")
        return

    set_config('current_project', proj_id)

def list_projects():
    all_projects = get_config('all_projects') or {}
    current = get_config('current_project')
    return [{
        "path": p,
        "is_current": all_projects[p] == current,
    } for p in all_projects]
