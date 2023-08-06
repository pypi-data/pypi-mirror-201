import inspect
import json
import os
import pathlib
import omegaconf
from typing import Optional, Tuple

import yaml


def get_files_in_directory(dir_path: str, filter_func: Optional[callable] = None) -> list:
    """Get paths of files in a directory
    :param dir_path: path of directory that you want to get files from
    :type dir_path: str
    :param filter_func: function that returns True if the file name is valid
    :type filter_func: callable
    :return: list of file paths in the directory which are valid
    :rtype: list
    """
    return [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and (filter_func is None or filter_func(f))]

def get_files_in_all_sub_directories(root_dir_path: str, filter_func: Optional[callable] = None) -> list:
    """Get paths of files in all sub directories
    :return: list of file paths in all sub directories which are valid
    :rtype: list
    """
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(root_dir_path) for f in filenames if (filter_func is None or filter_func(f))]

def create_directory(dir_path: str):
    """Creates all directories of the given path (if not exists)

    :param dir_path: directory path
    :type dir_path: str
    """
    return pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)

def read_json_file(file_path: str) -> dict:
    """Read a json file

    :param file_path: json file path
    :type file_path: str
    :return: json data
    :rtype: dict
    """
    with open(file_path, 'r') as f:
        return json.load(f)
    
def split_path_into_dir_and_file_name(file_path: str) -> Tuple[str, str]:
    """Split a file path into directory path and file name

    :param file_path: file path
    :type file_path: str
    :return: directory path and file name
    :rtype: Tuple[str, str]
    """
    return os.path.dirname(file_path), os.path.basename(file_path)

def read_yaml_file(file_path: str) -> dict:
    """Read a yaml file

    :param file_path: yaml file path
    :type file_path: str
    :return: yaml data
    :rtype: dict
    """
    with open(file_path, "r") as stream:
        try:
            return yaml.safe_load(stream) 
        except yaml.YAMLError as exc:
            print(exc)
            return None
        
def write_yaml_file(dict_object: dict, file_path: str) -> None:
    with open(file_path, 'w') as yaml_file:
        yaml.dump(dict_object, yaml_file, default_flow_style=False)


def path_from_current_file(relative_path: str) -> str:
    """convert relative path to absolute path with respect to the caller's file path"""
    file_path_of_caller = inspect.stack()[1].filename
    dir_path_of_caller = os.path.dirname(file_path_of_caller)
    full_path = os.path.join(dir_path_of_caller, relative_path)
    return os.path.normpath(full_path)

def load_config_file(file_path: str) -> omegaconf.OmegaConf:
    """Load a config file

    :param file_path: config file path
    :type file_path: str
    :return: config data
    :rtype: omegaconf.OmegaConf
    """
    return omegaconf.OmegaConf.load(file_path)

def write_config_file(config: omegaconf.OmegaConf, file_path: str) -> None:
    """Write a config file

    :param config: config data
    :type config: omegaconf.OmegaConf
    :param file_path: config file path
    :type file_path: str
    """
    omegaconf.OmegaConf.save(config, file_path)