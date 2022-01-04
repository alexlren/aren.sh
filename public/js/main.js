window.onload = function () {
    const themeSwitchBtn = document.getElementById('theme-switch');

    themeSwitchBtn.checked = !!localStorage.getItem(window.__LS_DARK_THEME_KEY);

    themeSwitchBtn.onchange = function () {
        const curTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = curTheme === 'dark' ? '' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        if (newTheme === 'dark') {
            localStorage.setItem(window.__LS_DARK_THEME_KEY, true);
        } else {
            localStorage.removeItem(window.__LS_DARK_THEME_KEY);
        }
    };
};
