class DBClientInterface:
    def create_index(self, index_name: str):
        raise NotImplementedError

    def delete_index(self, index_name: str):
        raise NotImplementedError

    def list_indices(self):
        raise NotImplementedError

    def get_index(self, index_name: str):
        raise NotImplementedError