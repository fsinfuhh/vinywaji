const colors = require('tailwindcss/colors')

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',
        '../templates/*.html',
    ],
    theme: {
        extend: {
            colors: {
                primary: colors.teal,
                neutral: colors.gray,
            },
            transitionProperty: {
                'floating': 'transform, color, padding, top',
            }
        },
    },
    safelist: [
        {
            pattern: /bg-(primary|gray|lime|orange)-(50|100|200|300|400|500|600|700|800|900|950)/,
            variants: ['hover', 'focus', 'dark', 'dark:hover', 'dark:focus'],
        },
    ],
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('tailwindcss/colors'),
    ],
}
