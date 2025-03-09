/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
      extend: {
        colors: {
          victorianBrown: "#2d1b0f",
          victorianGold: "#e0c097",
          victorianDark: "#3e2723",
          victorianBorder: "#9c6b3b",
          victorianAccent: "#d4a373",
        },
        fontFamily: {
          serif: ["Merriweather", "serif"],
        },
      },
    },
    plugins: [],
  };
  