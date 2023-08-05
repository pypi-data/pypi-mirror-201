class SecurityGroup(object):
    def __init__(self, security_group_id = None):
        self.security_group_id = security_group_id
        self.security_group_name = None
        self.region = None
        self.attached_resources = []

    
    def set_security_group_name(self, security_group_name):
        self.security_group_name = security_group_name


    def get_security_group_name(self):
        return self.security_group_name


    def get_security_group_id(self):
        return self.security_group_id


    def set_region_name(self, region_name):
        self.region_name = region_name

    
    def get_region_name(self):
        return self.region_name

    def add_attached_resource(self, resource_id):
        self.attached_resources.append(resource_id)

    
    def get_attached_resources(self):
        return self.attached_resources
