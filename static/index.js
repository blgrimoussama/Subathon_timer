const body = document.querySelector('body')
const sidebar = body.querySelector('.sidebar'),
    toggles = body.querySelectorAll('.toggle'),
    modeSwitch = body.querySelector('.toggle-switch'),
    modeText = body.querySelector('.mode-text'),
    mainPage = body.querySelector('.sibling'),
    TimerSettingsButton = body.querySelector('.timer-settings-button'),
    TimerButton = body.querySelector('.timer-button'),
    FontSettingsButton = body.querySelector('.font-settings-button'),
    FontButton = body.querySelector('.font-button');


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
    mainPage.classList = ['sibling settings'];
    hideTimerSiblings();
    s = mainPage.querySelector('#timer-settings').style
    s.opacity = 1;
    s.position = '';
})

FontSettingsButton.addEventListener('click', () => {
    mainPage.classList = ['sibling settings'];
    hideTimerSiblings();
    s = mainPage.querySelector('#font-settings').style
    s.opacity = 1;
    s.position = '';
})

TimerButton.addEventListener('click', () => {
    mainPage.classList = ['sibling'];
    hideTimerSiblings();
})

function hideTimerSiblings() {
    let timerSiblings = mainPage.querySelectorAll('.timer-sibling');
    timerSiblings.forEach(sibling => {
        sibling.style.opacity = 0;
        sibling.style.position = 'absolute';
    })
}