import { useOutletContext } from "react-router-dom";

type ContextType = { userApiKey?: string; externalUserId?: string };

export function useRootContext() {
  return useOutletContext<ContextType>();
}

export type PipelineFromAPI = {
  id: string;
  name: string;
  embedding_model: {
    type: "openai" | "huggingface";
  };
  vector_database: {
    type: "milvus" | "pinecone";
  };
  data_source: {
    type: "s3_text";
    url: string;
    splitter: {
      size: number;
      overlap: number;
    };
  };
};
