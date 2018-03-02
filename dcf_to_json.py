import json

# Types of lines
NODE = 1
KEY_VAL = 2

# Types of Node
LEVEL_ONE = ['dictionary', "languages", "level", "record"]
LEVEL_TWO = ['item', 'valueset']


def get_line_type(line):
    if not line:
        return None
    if line[0] == "[" and line[-1] == "]":
        return NODE

    if "=" in line:
        return KEY_VAL
    return None


def clean_node(line):
    if get_line_type(line) == NODE:
        return line.strip("[").strip("]")

    else:
        meta_dict = {}
        key, value = line.split("=")
        meta_dict[key] = value.strip("'")
        return meta_dict


def get_node_children(lines, level):
    children = []
    for i in range(0, len(lines)):
        line = lines[i]
        if get_line_type(line) == NODE:
            if get_level(line) == level:
                children.append(get_node(lines[i:], level))
            if get_level(line) < level:
                break
    return children


def get_node_values(lines):
    attributes = {}
    for line in lines:
        if get_line_type(line) == KEY_VAL:
            attributes.update(clean_node(line))
        elif get_line_type(line) == NODE:
            break
    return attributes


def get_node(lines, level):
    node_name = clean_node(lines[0])
    node = {"node_name": node_name}
    node_meta = get_node_values(lines[1:])
    node.update(node_meta)
    children = get_node_children(lines[1:], level + 1)
    if len(children) > 0:
        node['children'] = children
    return node


def get_level(node):
    node_name = clean_node(node)
    if node_name.lower() in LEVEL_ONE:
        return 1
    else:
        return 2


def main(input_file, output_file):
    with open(input_file) as f:
        content = f.readlines()
    lines = [x.strip() for x in content]
    data = get_node_children(lines, 1)
    with open(output_file, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    input_file = "input.dcf"
    output_file = "output.json"
    main(input_file, output_file)
