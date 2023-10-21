import { Turbine } from "./src/turbine";

const turbine = new Turbine("test");

turbine.createProject({
  dataSource: {
    type: "postgres",
    config: {
      url: "postgres://postgres:postgres@localhost:5432/postgres",
      table: "user_tweets",
    },
    fields: ["user_bio", "tweet_text"],
  },
  embeddingModel: "text-embedding-ada-002",
  vectorDb: "pinecone",
});
