import type { Config } from "tailwindcss";
export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      screens: {
        // Mobile Devices
        "mobile-xs": { min: "320px" },
        "mobile-xs-max": { max: "319px" },

        "mobile-sm": { min: "375px" },
        "mobile-sm-max": { max: "374px" },

        "mobile-md": { min: "414px" },
        "mobile-md-max": { max: "413px" },

        "mobile-lg": { min: "480px" },
        "mobile-lg-max": { max: "479px" },

        "mobile-xl": { min: "540px" },
        "mobile-xl-max": { max: "539px" },

        // Tablet Devices
        "tablet-sm": { min: "600px" },
        "tablet-sm-max": { max: "599px" },

        tablet: { min: "768px" },
        "tablet-max": { max: "767px" },

        "tablet-lg": { min: "900px" },
        "tablet-lg-max": { max: "899px" },

        // Laptop Devices
        laptop: { min: "1024px" },
        "laptop-max": { max: "1023px" },

        "laptop-lg": { min: "1280px" },
        "laptop-lg-max": { max: "1279px" },

        "laptop-xl": { min: "1440px" },
        "laptop-xl-max": { max: "1439px" },

        // Desktop Devices
        desktop: { min: "1600px" },
        "desktop-max": { max: "1599px" },

        "desktop-lg": { min: "1920px" },
        "desktop-lg-max": { max: "1919px" },

        // 4K Devices
        "4k": { min: "2560px" },
        "4k-max": { max: "2559px" },
      },
      keyframes: {
        "spin-border": {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        spin: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        "spin-fast-middle": {
          "0%": { transform: "rotate(0deg)" },
          "50%": { transform: "rotate(180deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
      },
      animation: {
        "spin-slow": "spin 10s linear infinite",
        "spin-medium": "spin 5s linear infinite",
        "spin-fast": "spin 3s linear infinite",
        "spin-border": "spin-border 5s linear infinite",
      },
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: "var(--primary)",
        primaryLight: "var(--primary-light)",
        primaryDark: "var(--primary-dark)",
        secondary: "var(--secondary)",
        textDark: "var(--text-dark)",
        shadowPrimary: "var(--shadow-primary)",
      },
      boxShadow: {
        bottom: "0 4px 6px rgba(0, 0, 0, 0.1)",
      },
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
      },
      backgroundImage: {
        "custom-svg": "url('/images/homepage/bg.svg')",
        grid: "url('/grid.svg')",
      },
    },
  },
  plugins: [],
} satisfies Config;
