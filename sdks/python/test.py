from turbine import Turbine, ProjectConfig, DataSource, PostgresConfig

turbine = Turbine("your-api-key")

project_id = turbine.create_project(
    ProjectConfig(
        data_source=DataSource(
            type="postgres",
            config=PostgresConfig(
                url="postgres://user:password@hostname:port/database",
                table="user_tweets",  # table to index
            ),
            fields=["user_bio", "tweet_text"],  # columns to index
        ),
        vector_db="pinecone",
        embedding_model="text-embedding-ada-002",
    )
)

>> turbine.search(project_id, "your search query")
[
    SearchResult(
        id='5512',
        score=0.82
    ),
    SearchResult(
        id='10311',
        score=0.78
    ),
]
