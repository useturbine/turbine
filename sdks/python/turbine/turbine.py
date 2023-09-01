from turbine_sdk.turbine.api import project, search


class Turbine:
    def __init__(self, token):
        self.turbine_systems = None
        self.project_api = project.ProjectAPI(token)
        self.search_api = search.SearchAPI(token)

    def create_project(self, project_data, _async=False):
        if _async:
            return self.project_api.create_project_async(project_data)

        return self.project_api.create_project(project_data)

    def get_project(self, project_id=None, _async=False):
        if _async:
            return self.project_api.get_project_async(project_id)

        return self.project_api.get_project(project_id)

    def update_project(self, project_id, project_data, _async=False):
        if _async:
            return self.project_api.update_project_async(project_id, project_data)

        return self.project_api.update_project(project_id, project_data)

    def delete_project(self, project_id, _async=False):
        if _async:
            return self.project_api.delete_project_async(project_id)

        return self.project_api.delete_project(project_id)

    def search(self, **args):
        return self.search_api.search(**args)

    def status(self):
        return self.turbine_systems.status()
