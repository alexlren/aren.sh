const LS_DARK_THEME_KEY = 'dark_theme';
const darkTheme = !!localStorage.getItem(LS_DARK_THEME_KEY);
const themeSwitchBtn = document.getElementById('theme-switch');

if (darkTheme) {
    document.documentElement.setAttribute('data-theme', 'dark');
    themeSwitchBtn.checked = true;
}


themeSwitchBtn.onchange = function () {
    const curTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = curTheme === 'dark' ? '' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    if (newTheme === 'dark') {
        localStorage.setItem(LS_DARK_THEME_KEY, true);
    } else {
        localStorage.removeItem(LS_DARK_THEME_KEY);
    }
};
