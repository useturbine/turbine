from turbine import Turbine, ProjectConfig

turbine = Turbine(
    api_key="test",
    base_url="http://localhost/v1",
)
# projects = turbine.get_projects()
# print(projects)


project = turbine.get_project("1")
print(project.config.embedding_model)


project_id = turbine.create_project(
    ProjectConfig(
        **{
            "data_source": {
                "type": "postgres",
                "config": {
                    "host": "db.afihywbgjjjvpqvjosog.supabase.co",
                    "port": 5432,
                    "user": "postgres",
                    "database": "postgres",
                    "password": "9KSiivip@iRZiqT",
                    "table": "public.users",
                },
            },
            "embedding_model": "openai",
            "vector_db": "milvus",
            "similarity_metric": "cosine",
        }
    )
)
print(project_id)
