import git
import logconf
import logging
import magic
import os
import platform
import re
import subprocess
import traceback

def _verify_libmagic():
    try:
        magic.Magic().from_file(__file__)
    except Exception as e:
        print("Please install libmagic library on your computer:")
        if platform.system() == "Linux":
            print("sudo apt install libmagic-dev libmagic1")
        elif platform.system() == "Darwin":
            print("brew install libmagic")

        exit(-1)

_verify_libmagic()

_FILTER_LOG_ENABLED = False # TODO move to config file
MAX_FILE_LEN = 300000
MAGIC_OBJ = magic.Magic(mime=True)
GIT_FILES_LIST = None
GITIGNORE_PATH = None
JS_FUNC_OR_CLASS = re.compile(
    r"(export\s+)?(class|function)\s+[A-Za-z0-9_$]+\s*"
    r"|[\w\s]*=[\s]*(async\s+)?(\([\w\s,]*\)|\w+)\s*=>"
    r"|\w+\s*=\s*\([^\)]*\)\s*=>"
    r"|(export\s+default\s+\(state\s*=\s*initialState,\s*action\)\s*=>)"
)

def is_single_line(filepath):
    with open(filepath) as f:
        line = f.readline()
        for remaining_line in f:
            if remaining_line.strip() != '':
                return False

        return True

def is_empty(filepath):
    if not os.path.isfile(filepath):
        return False

    with open(filepath) as f:
        return not any(line.strip() for line in f)

def isnt_utf8(filepath):
    try:
        with open(filepath) as fp:
            fp.readline()
    except UnicodeDecodeError:
        return True
    return False

def is_gitdir(filepath):
    return "/.git/" in filepath

def valid_mime(filepath):
    ignored_types = {
        'application/font',
        'application/gzip',
        'application/java-archive',
        'application/json',
        'application/msword',
        'application/octet-stream',
        'application/ogg',
        'application/pdf',
        'application/pgp-keys',
        'application/postscript',
        'application/vnd.adobe.flash-movie',
        'application/vnd.android.package-archive',
        'application/vnd.apple.mpegurl',
        'application/vnd.ms-',
        'application/vnd.oasis.',
        'application/vnd.openxmlformats-officedocument.',
        'application/x-7z-compressed',
        'application/x-bzip2',
        'application/x-compressed-tar',
        'application/x-deb',
        'application/x-dosexec',
        'application/x-dvi',
        'application/x-executable',
        'application/x-font-otf',
        'application/x-font-ttf',
        'application/x-java-archive',
        'application/x-java-keystore',
        'application/x-mach-binary',
        'application/x-mpegURL',
        'application/x-ms-shortcut',
        'application/x-msdownload',
        'application/x-msi',
        'application/x-object',
        'application/x-rar-compressed',
        'application/x-rpm',
        'application/x-sharedlib',
        'application/x-shockwave-flash',
        'application/x-tar',
        'application/x-xz',
        'application/zip',
        'application/zlib',
        'application/zstd',
        'audio',
        'font/',
        'image',
        'inode/x-empty',
        'text/x-po',
        'video',
    }

    file_type = MAGIC_OBJ.from_file(filepath)
    return not any(file_type.startswith(ignored_type) for ignored_type in ignored_types)

def _init_git_files(project_path):
    logging.debug(f"initializing git files list for project {project_path}")
    if not os.path.exists(os.path.join(project_path, '.gitignore')):
        logging.warning(".gitignore doesn't exist, skipping")
        return []

    try:
        repo = git.Repo(project_path)
    except git.exc.InvalidGitRepositoryError:
        logging.warning("failed to read repository")
        return []

    files = [f for f in repo.untracked_files]
    files += [f for f in repo.git.ls_files(
        '--exclude-standard').split('\n') if f]
    return [os.path.join(project_path, f) for f in files]

def update_gitignore(project_path):
    global GIT_FILES_LIST, GITIGNORE_PATH
    logging.debug(f"Updating gitignore cache for {project_path}")

    if project_path == GITIGNORE_PATH:
        return

    GIT_FILES_LIST = _init_git_files(project_path)
    GITIGNORE_PATH = project_path

def is_gitignored(file_path, project_path): # TODO
    global GIT_FILES_LIST
    if GIT_FILES_LIST is None:
        GIT_FILES_LIST = _init_git_files(project_path)
    if GIT_FILES_LIST == []:
        return False

    return file_path not in GIT_FILES_LIST

def is_js_data(file_path):
    if ".js" not in file_path:
        return False

    try:
        with open(file_path) as fp:
            code = fp.read()

        if "StyleSheet.create" in code:
            return False

        matches = JS_FUNC_OR_CLASS.findall(code, re.MULTILINE)
        if _FILTER_LOG_ENABLED:
            logging.debug(f"file {file_path} matched {matches}")
        count = len(matches)

    except:
        logging.warn("Error while scanning .js file:\n" + traceback.format_exc())
        return False

    return count == 0

def ignored_extension(file_path):
    _, ext = os.path.splitext(file_path)
    ignore = ['.csv', '.tsv', '.pem', '.cer', '.key', '.log']
    return ext in ignore

def _filter_log(reason, outcome, path):
    if _FILTER_LOG_ENABLED:
        logging.debug(f"Filter {outcome} due to {reason} for path {path}")

def should_ignore(filepath, project_path):
    if os.path.isdir(filepath):
        _filter_log("IS_DIR", False, filepath)
        return False
    if os.path.islink(filepath):
        _filter_log("IS_LINK", True, filepath)
        return True
    if ignored_extension(filepath):
        _filter_log("IGNORE_EXT", True, filepath)
        return True
    if is_gitignored(filepath, project_path):
        _filter_log("GITIGNORE", True, filepath)
        return True
    if is_gitdir(filepath):
        _filter_log("IN_GITDIR", True, filepath)
        return True
    if not valid_mime(filepath):
        _filter_log("INVALID_MIME", True, filepath)
        return True
    if os.path.getsize(filepath) >= MAX_FILE_LEN:
        _filter_log("TOO_LARGE", True, filepath)
        return True
    if isnt_utf8(filepath):
        _filter_log("BINARY_FILE", True, filepath)
        return True
    if is_single_line(filepath):
        _filter_log("SINGLE_LINE", True, filepath)
        return True
    if is_empty(filepath):
        _filter_log("IS_EMPTY", True, filepath)
        return True
    if is_js_data(filepath):
        _filter_log("IS_JS_DATA", True, filepath)
        return True

    _filter_log("PASSED_CHECKS", False, filepath)
    return False
