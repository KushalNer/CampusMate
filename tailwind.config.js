/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/*.html',
    './CampusMateApp/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'slate-grey': '#404F68',
        'pale-slate': '#7A859D',
        'misty-grey': '#B9C1D0',
        'silver-grey': '#C4C4C4',
        'cloud-white': '#F2F2F2',
      },
    },
  },
  plugins: [],
}
