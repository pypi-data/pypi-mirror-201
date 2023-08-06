

class InvalidTaskStatus(Exception):

    required_status, instance_status = None, None

    def __init__(self, required_status, instance_status):
        self.required_status = required_status
        self.instance_status = instance_status

    def __str__(self):
        return f'required task status({self.required_status}) != instance status({self.instance_status})'
