import os
import yaml
import logging
from hashlib import md5
ROOT_PATH = os.path.realpath(os.curdir)
__levels_or_log = {
 'CRITICAL' : 50, 
 'ERROR' : 40,
 'WARNING' : 30,
 'INFO' : 20,
 'DEBUG' : 10,
 'NOTSET' : 0,
}


class YamlConfig:
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        self.load()

    def load(self):
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as f:
                self.config = yaml.safe_load(f)
        elif os.path.isdir(self.filename):
            self.config = self._merge_yaml_files(self.filename)
        else:
            raise ValueError(f"{self.filename} is not a file or directory")

    def save(self):
        with open(self.filename, "w") as f:
            yaml.safe_dump(self.config, f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def delete(self, key):
        del self.config[key]

    def _merge_dicts(self, dict1, dict2):
        for key in dict2:
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                dict1[key] = self._merge_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        return dict1

    def _merge_yaml_files(self, dir_path):
        global _log
        merged_config = {}
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".yaml"):
                file_config = self._load_yaml_file(file_path)
                if isinstance(file_config, dict):
                    merged_config = self._merge_dicts(merged_config, file_config)
                # else:
                #     _log.warn(f"YAML file {file_path} must contain a dictionary")
            elif os.path.isdir(file_path):
                dir_config = self._merge_yaml_files(file_path)
                merged_config = self._merge_dicts(merged_config, dir_config)
        return merged_config

    def _load_yaml_file(self, filename):
        with open(filename, "r") as f:
            return yaml.safe_load(f)

config = YamlConfig(os.path.join(ROOT_PATH,"configs") )

__log_level = config.get('log')['level'] or 'DEBUG'
logging.basicConfig(level=__levels_or_log[__log_level])
_log = logging.getLogger(config.get("log")['name'] or "FastApi Framework")