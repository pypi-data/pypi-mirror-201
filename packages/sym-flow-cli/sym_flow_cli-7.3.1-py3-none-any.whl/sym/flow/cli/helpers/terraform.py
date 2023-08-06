from typing import Any, Optional


def get_terraform_resource(file_contents: dict, type_: str, name: str) -> Optional[dict]:
    """Get a specific Terraform resource, represented as a dictionary parsed by hcl2,
    from a Terraform file's contents. If the particular element cannot be found, returns
    None.

    For example, if you have the following Terraform resource:

        resource "sym_flow" "my_flow" {
            ...
        }

    Then the type_ is "sym_flow", and the name is "my_flow".

    Args:
        file_contents: A dictionary representing the contents of a Terraform file as parsed by hcl2.
        type_: The type of Terraform resource to look for (e.g. sym_integration, sym_flow).
        name: The name of the Terraform resource to look for (eg. "my_flow", "this").

    Example hcl2-parsed structure:
    {
        "resource": [
            {"sym_integration": {"name": "prod-slack"}},
            {"sym_integration": {"name": "dev-slack"}},
            {"sym_environment": {"name": "prod"}},
            ...
        ],
        "locals": [
            {"environment_name": "one"}
        ],
        ...
    }
    """

    # If we can't find any resources, consider the lookup a failure.
    if not (resources := file_contents.get("resource")):
        return None

    # Resources of the same type are not grouped, they will be different items in the list
    # of resources. So look at each of them, make sure they're the right type, and then also
    # check their name. If both match, return it.
    for r in resources:
        if r.get(type_) and r[type_].get(name):
            return r[type_][name]

    # We didn't find what we were looking for, so this lookup was a failure.
    return None


def get_terraform_local_variable(file_contents: dict, name: str) -> Any:
    """Get the value of a variable from any `locals` block in the given Terraform file,
    represented as a dictionary parsed by hcl2. If the particular variable cannot be found,
    returns None.

    Local variable names must be unique per-module, so there is guaranteed to only be one
    at maximum in the given file_contents, even if there are multiple locals blocks.

    Args:
        file_contents: A dictionary representing the contents of a Terraform file as parsed by hcl2.
        name: The name of the local variable to look for (eg. "environment_name", "aws_region").

    Returns:
        The value of the local variable, or None if it cannot be found. This may be
        any Terraform-valid type.
    """

    if not (tf_locals := file_contents.get("locals")):
        return None

    for block in tf_locals:
        # False is allowed, so we must check explicitly for None.
        if (value := block.get(name)) is not None:
            return value

    return None


def get_terraform_module(file_contents: dict, name: str) -> Optional[dict]:
    """Get the value of a module from the given Terraform file, represented as
    a dictionary parsed by hcl2. If the particular module name cannot be found,
    returns None.
    """

    if not (modules := file_contents.get("module")):
        return None

    return next((m[name] for m in modules if m.get(name)), None)
