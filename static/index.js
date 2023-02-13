const body = document.querySelector('body')
const sidebar = body.querySelector('.sidebar'),
toggles = body.querySelectorAll('.toggle'),
modeSwitch = body.querySelector('.toggle-switch'),
modeText = body.querySelector('.mode-text'),
mainPage = body.querySelector('.sibling'),
TimerSettingsButton = body.querySelector('.timer-settings-button'),
TimerButton = body.querySelector('.timer-button');


toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('close');
    });
});


modeSwitch.addEventListener('click', () => {
    body.classList.toggle('dark');

    if (body.classList.contains('dark')) {
        modeText.innerHTML = 'Light Mode';
    } else {
        modeText.innerHTML = 'Dark Mode';
    }

});

TimerSettingsButton.addEventListener('click', () => {
    mainPage.classList = ['sibling timer-settings'];
    s = mainPage.querySelector('#timer-settings').style
    s.opacity = 1;
    s.position = '';
})

TimerButton.addEventListener('click', () => {
    mainPage.classList = ['sibling'];
    s = mainPage.querySelector('#timer-settings').style
    s.opacity = 0;
    s.position = 'absolute';
})