import types
import re
from google.protobuf.any_pb2 import Any

# Define a function to convert camelCase to snake_case
def camel_to_snake(name):
    # Use a regular expression to match uppercase letters
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    # Split the name into words and join them with underscores
    snake_name = pattern.sub('_', name).lower()
    return snake_name

# Define a function to recursively convert JSON attributes to snake_case
def snake_case_json(obj):
    if isinstance(obj, dict):
        # Create a new dictionary with snake_case keys
        new_dict = {}
        for key, value in obj.items():
            new_key = camel_to_snake(key)
            new_value = snake_case_json(value)
            new_dict[new_key] = new_value
        return new_dict
    elif isinstance(obj, list):
        # Recursively convert each item in the list
        return [snake_case_json(item) for item in obj]
    else:
        # Return the original value
        return obj

def unpack_grpc_resource(data: Any, resource_type):
    resource = resource_type()
    # data.Unpack(resource) # Unpack verify the object DESCRIPTOR that can differ if generated protos version differs
    resource.ParseFromString(data.value)
    return resource