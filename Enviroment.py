"""
    Environment: names storage.
"""
class Environment:
    """
    Creates an environment with the given record.
    """
    def __init__(self, record = {}, parent = None):
        self.record = record
        self.parent = parent

    """
    Creates a variable with the given name and value.

    :param name: The variable name (key).
    :param value: The value associated with the name.
    :return: The value assigned.
    """
    def define(self, name, value):
        self.record[name] = value
        return value
    
    """
    Updates an existing variable.
    """
    def assign(self, name, value):
        env = self.resolve(name)
        env.record[name] = value # update the variable with the new value.
        return value
    
    """
    Returns the value of a defined variable, or throws
    if variable is not defined.
    """
    def lookup(self, name):
        return self.resolve(name).record[name]
        
    """
    Returns specific environment in which a variable is defined, or
    throws if a variable is not defined.
    """
    def resolve(self, name):
        # If the variable is defined in the current environment, return it.
        if name in self.record:
            return self
        # Otherwise, if there is a parent, recursively check the parent.
        elif self.parent is not None:
            return self.parent.resolve(name)
        # If there is no parent and the variable is not found, throw an error.
        else:
            raise ReferenceError(f'Variable {name} is not defined.')