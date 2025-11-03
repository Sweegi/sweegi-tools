/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#d3139c', // 主要颜色
          600: '#be185d',
          700: '#9d174d',
          800: '#831843',
          900: '#701a75',
        }
      }
    },
  },
  plugins: [],
  // 防止与Element Plus冲突
  corePlugins: {
    preflight: false,
  }
} 