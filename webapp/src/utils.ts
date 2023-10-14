import { useOutletContext } from "react-router-dom";

type ContextType = { userApiKey?: string; externalUserId?: string };

export function useRootContext() {
  return useOutletContext<ContextType>();
}
