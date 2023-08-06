import ast


def to_list(node):
    return [
        node.__class__.__name__,
        *((field, handle_field(value)) for field, value in ast.iter_fields(node)),
    ]


def handle_field(field):
    if isinstance(field, ast.AST):
        return to_list(field)
    elif isinstance(field, list):
        return [to_list(x) for x in field]
    else:
        return field
