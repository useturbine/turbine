import { Turbine } from "./src";
// import { Turbine } from "@useturbine/turbine";

const main = async () => {
  const turbine = new Turbine("test");

  const projectId = await turbine.createProject({
    dataSource: {
      type: "postgres",
      config: {
        host: "db.afihywbgjjjvpqvjosog.supabase.co",
        port: 5432,
        user: "postgres",
        database: "postgres",
        password: "9KSiivip@iRZiqT",
        table: "public.users",
      },
    },
    embeddingModel: "openai",
    vectorDB: "milvus",
    similarityMetric: "cosine",
  });
  console.log(projectId);

  const results = await turbine.search("1", "test", 10);
  console.log(results);
};

main();
