/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../**/templates/**/*.html',
    '../../templates/**/*.html',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        slateGrey: '#404F68',   // Primary
        paleSlate: '#7A859D',   // Secondary
        mistyGrey: '#B9C1D0',   // Card background
        silverGrey: '#C4C4C4',  // Borders / Inputs
        cloudWhite: '#F2F2F2',  // Background
      },
    },
  },
  plugins: [],
}
