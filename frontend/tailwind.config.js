/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#141b2d",
        secondary: "#1f2a40",
        accent: "#3b82f6",
      },
    },
  },
  plugins: [],
}
