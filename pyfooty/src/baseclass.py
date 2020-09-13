from abc import ABCMeta, abstractmethod

class AbstractFooty(metaclass = ABCMeta): 
    """ Abstract class for PyRef data. Should be inherited for all other
    classes

    """

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod
    def valid_tables(self, fbref_url, name):
        pass

    @abstractmethod
    def get_table(self, table_type):
        pass

    @abstractmethod
    def get_tables(self):
        pass
