import yaml
from dotmap import DotMap


def read_yaml_file(file):
    with open(file, "r") as stream:
        try:
            return DotMap(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
            return {}
