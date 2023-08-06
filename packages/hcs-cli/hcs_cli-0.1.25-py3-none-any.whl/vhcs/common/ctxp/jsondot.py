"""
jsondot is utility to make json/dict object accessible in the "." way.

##########
#Example 1: load, update, and save JSON file
##########

data = jsondot.load('path/to/my.json')
print(data.hello.message)
data.hello.message = 'Hello, mortal.'
jsondot.save(data, 'path/to/my.json')
	

##########
#Example 2: decorate an existing python dict
##########

my_dict = jsondot.dotify(my_dict)
print(my_dict.key1.key2)
"""

import json
import os.path


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def dotify(target: any) -> any:
    """Deeply convert an object from dict to dotdict"""

    # If already dotified, skip
    if isinstance(target, dotdict):
        return target
    if isinstance(target, list):
        for i in range(len(target)):
            target[i] = dotify(target[i])
        return target
    if isinstance(target, dict):
        for k in target:
            target[k] = dotify(target[k])
        return dotdict(target)

    # Return unchanged
    return target


def _is_primitive(obj):
    return isinstance(obj, str) or isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float)


def plain(target: any) -> any:
    """Deeply convert a dotdict from dict"""
    if _is_primitive(target):
        return target

    if isinstance(target, list):
        for i in range(len(target)):
            target[i] = plain(target[i])
        return target
    if isinstance(target, dict):
        for k in target:
            target[k] = plain(target[k])
        return dict(target)


def load(file: str, default=None) -> dotdict:
    if not os.path.exists(file):
        return default
    with open(file) as json_file:
        dict = json.load(json_file)
    return dotify(dict)


def parse(text: str) -> dotdict:
    dict = json.loads(text)
    return dotify(dict)


def save(data: dict, file, format=True) -> None:
    with open(file, "w") as outfile:
        if format:
            json.dump(data, outfile, indent="\t")
        else:
            json.dump(data, outfile)
