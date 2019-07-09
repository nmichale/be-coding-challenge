import json
import yaml
import collections

def yaml_to_json(fn):
    # Setup support for ordered dicts so we do not lose ordering
    # when importing from YAML
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_mapping(_mapping_tag, data.iteritems())

    def dict_constructor(loader, node):
        return collections.OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(collections.OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)

    data = yaml.load(open(fn), Loader=yaml.FullLoader)
    return json.dumps(data, indent=2)