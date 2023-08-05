import re
from os.path import join

import bagit


def validate(bag_path):
    """Validates a bag against the BagIt specification"""
    bag = bagit.Bag(bag_path)
    return bag.validate()


def update_bag_info(bag_path, data):
    """Adds metadata from a dictionary to `bag-info.txt`"""
    assert(isinstance(data, dict))
    bag = bagit.Bag(bag_path)
    for k, v in data.items():
        bag.info[k] = v
    bag.save()


def update_manifests(bag_path):
    """Updates bag manifests according to BagIt specification"""
    bag = bagit.Bag(bag_path)
    bag.save(manifests=True)


def get_bag_info_fields(bag_path):
    """Returns """
    fields = {}
    patterns = ["(?P<key>[\\w\\-]+)", "(?P<val>.+)"]
    try:
        with open(join(bag_path, "bag-info.txt"), "r") as f:
            for line in f.readlines():
                line = line.strip("\n")

                row_search = re.search(":?(\\s)?".join(patterns), line)
                if row_search:
                    key = row_search.group("key").replace("-", "_").strip()
                    val = row_search.group("val").strip()
                    if key in fields:
                        listval = [fields[key]]
                        listval.append(val)
                        fields[key] = listval
                    else:
                        fields[key] = val
    except FileNotFoundError:
        print("Could not find a bag-info.txt file at {}".format(
            join(bag_path, "bag-info.txt")))
    return fields
