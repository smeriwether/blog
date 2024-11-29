/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./blog/templates/**/*.html'],
  darkMode: 'media',
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: 'inherit',
            a: {
              color: '#3b82f6', // blue-500
              '&:hover': {
                color: '#2563eb', // blue-600
              },
              textDecoration: 'none',
            },
            strong: {
              color: 'inherit',
            },
            h1: {
              color: 'inherit',
            },
            h2: {
              color: 'inherit',
            },
            h3: {
              color: 'inherit',
            },
            h4: {
              color: 'inherit',
            },
            code: {
              color: 'inherit',
            },
            blockquote: {
              color: 'inherit',
              borderLeftColor: '#e5e7eb', // gray-200
            },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
