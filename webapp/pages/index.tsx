import { Inter } from "next/font/google";
import { Button, Center } from "@mantine/core";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <Center m="lg" className={inter.className}>
      <Button variant="outline">Login with Google</Button>
    </Center>
  );
}
