window.__LS_THEME_KEY = 'current_theme';

const setThemeMode = (mode) => {
    document.documentElement.setAttribute('data-theme', mode);
};

const getSavedTheme = () => {
    return localStorage.getItem(window.__LS_THEME_KEY) === 'dark' ? 'dark' : 'light';
};

const saveCurrentTheme = (newTheme) => {
    localStorage.setItem(window.__LS_THEME_KEY, newTheme);
};

window.onload = function () {
    const themeSwitchBtn = document.getElementById('theme-switch');

    themeSwitchBtn.onchange = () => {
        const curTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = curTheme === 'dark' ? 'light' : 'dark';

        saveCurrentTheme(newTheme);
        setThemeMode(newTheme);
    };

    const theme = getSavedTheme();
    themeSwitchBtn.checked = theme === 'dark';
};

const savedTheme = getSavedTheme();
setThemeMode(savedTheme);
