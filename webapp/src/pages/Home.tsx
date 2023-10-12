import { useDisclosure } from "@mantine/hooks";
import { AppShell, Burger, Group, Image, Text } from "@mantine/core";
import { UserButton, useUser } from "@clerk/clerk-react";
import { useState, useEffect } from "react";
import { turbineAdminApiKey, turbineApiUrl } from "../config";

export const Home = () => {
  const [opened, { toggle }] = useDisclosure();
  const { user } = useUser();
  const [apiKey, setApiKey] = useState<string | null>(null);

  // Fetch user's API key
  useEffect(() => {
    const fetchApiKey = async () => {
      if (user) {
        const response = await fetch(`${turbineApiUrl}/users/${user.id}`, {
          headers: {
            "X-Turbine-Key": turbineAdminApiKey,
          },
        });
        const data = await response.json();
        setApiKey(data.api_key);
      }
    };

    fetchApiKey();
  }, [user]);

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{ width: 300, breakpoint: "sm", collapsed: { mobile: !opened } }}
      padding="md"
    >
      <AppShell.Header>
        <Group justify="space-between" h="100%" px="md">
          <Group>
            <Burger
              opened={opened}
              onClick={toggle}
              hiddenFrom="sm"
              size="sm"
            />
            <Image src="/images/turbine.png" width={30} height={30} />
            <Text size="xl">Turbine</Text>
          </Group>
          <UserButton />
        </Group>
      </AppShell.Header>
      <AppShell.Navbar p="md">Indices</AppShell.Navbar>
      <AppShell.Main>Main</AppShell.Main>
    </AppShell>
  );
};
