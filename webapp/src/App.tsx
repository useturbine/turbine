import { ClerkProvider, SignedIn, SignedOut } from "@clerk/clerk-react";
import "@mantine/core/styles.css";
import { MantineProvider } from "@mantine/core";
import { Home } from "./pages/Home";
import { LogIn } from "./pages/LogIn";

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

function App() {
  return (
    <ClerkProvider publishableKey={clerkPubKey}>
      <MantineProvider>
        <SignedIn>
          <Home />
        </SignedIn>
        <SignedOut>
          <LogIn />
        </SignedOut>
      </MantineProvider>
    </ClerkProvider>
  );
}

export default App;
