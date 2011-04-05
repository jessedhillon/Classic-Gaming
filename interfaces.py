class RomNotFoundException(Exception):
    pass

class RomIdentifier(object):
    system = None
    query = None

    def __init__(self, system, query):
        self.system = system
        self.query = query

    def get_title(self):
        pass

    def get_description(self):
        pass

    def get_publisher(self):
        pass

    def get_year(self):
        pass

    def get_image(self):
        pass
