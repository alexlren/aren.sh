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

const setupThemeSwitch = () => {
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

const setupToc = () => {
    tocbot.init({
        tocSelector: '.toc-container',
        contentSelector: '.content',
        headingSelector: 'h1, h2, h3, h4, h5',
        collapseDepth: 1,
        orderedList: false,
        scrollSmooth: true,
        headingsOffset: 200,
    });
};

window.onload = function () {
    setupThemeSwitch();
    setupToc();
};

const savedTheme = getSavedTheme();
setThemeMode(savedTheme);
