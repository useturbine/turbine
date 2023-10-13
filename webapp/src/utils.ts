import { useOutletContext } from "react-router-dom";

type ContextType = { userApiKey: string | null };

export function useRootContext() {
  return useOutletContext<ContextType>();
}
