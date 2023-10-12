import {
  ClerkProvider,
  SignedIn,
  SignedOut,
  UserButton,
  SignIn,
} from "@clerk/clerk-react";

if (!import.meta.env.VITE_CLERK_PUBLISHABLE_KEY)
  throw new Error("Missing Clerk Publishable Key");

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

function App() {
  return (
    <ClerkProvider publishableKey={clerkPubKey}>
      <SignedIn>
        <div>You are signed in!</div>
        <UserButton />
      </SignedIn>
      <SignedOut>
        <SignIn />
      </SignedOut>
    </ClerkProvider>
  );
}

export default App;
