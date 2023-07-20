import { Box, Button, Group, Stack, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";
import axios from "axios";
import { useState } from "react";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const form = useForm({
    initialValues: {
      email: "",
      name: "",
    },

    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
    },
  });

  const register = async (values: typeof form.values) => {
    const client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL,
    });
    setLoading(true);

    // Make POST request to backend register endpoint
    try {
      await client.post("/register", values);
    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  return (
    <Box maw={300} mx="auto">
      <form onSubmit={form.onSubmit(register)}>
        <Stack spacing="xs">
          <TextInput
            withAsterisk
            label="Email"
            placeholder="your@email.com"
            {...form.getInputProps("email")}
          />
          <TextInput
            label="Name"
            placeholder="Your Name"
            {...form.getInputProps("name")}
          />
        </Stack>

        <Group position="right" mt="md">
          <Button type="submit" loading={loading}>
            Sign Up
          </Button>
        </Group>
      </form>
    </Box>
  );
}
