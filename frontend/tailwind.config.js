/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: "#0f172a",
        glass: "rgba(255, 255, 255, 0.05)",
        fraud: "#ef4444",
        legit: "#10b981",
      },
      backdropBlur: {
        xs: "2px",
      }
    },
  },
  plugins: [],
}
