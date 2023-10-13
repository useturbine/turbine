/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.tsx",
    "node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}",
  ],
  plugins: [require("flowbite/plugin")],
  theme: {
    extend: {},
  },
};
