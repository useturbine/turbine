from abc import abstractmethod


class DataSource:
    @abstractmethod
    def get_all_documents(self):
        pass

    @abstractmethod
    def get_new_documents(self):
        pass
