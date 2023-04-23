// Set the initial time for the timer
let time = 0; // 10 hours in seconds
let FirstTime = true;
// Create an EventSource to receive updates to the deadline
let eventSource = new EventSource("/sse");
let realTime = 0;
let deadline = 0;
let interval;


window.onbeforeunload = function() {
  console.log("Closing SSE connection");
  eventSource.close();
}

let timer_div = document.getElementById('timer');

// Set an event listener for when the deadline is updated
eventSource.addEventListener("deadline", function(event) {
  deadline = new Date(JSON.parse(event.data).deadline).getTime(); // Get the deadline as a Unix timestamp
  let currentTime = Date.now(); // Get the current time as a Unix timestamp
  let timeDiff = Math.floor((deadline - currentTime) / 1000); // Calculate the time remaining, capped at 0
  if (FirstTime) {
    time = timeDiff;
  }
  realTime = (realTime === time || !realTime) ? time : realTime;

  // Get the input value and add it to the time slowly with an animation
  let input = timeDiff - realTime; // Set the input value to the time remaining, capped at 0
  let timer_caller = '';
  if (!FirstTime) {
    if (input < 0) {
      timer_caller = 'neg_time';
    } else {
      timer_caller = 'pos_time';
    }
    timer_div.classList.add(timer_caller);
  }
  else {
    FirstTime = false;
  }
  realTime = Math.floor((deadline - currentTime) / 1000);
  let startTime = Date.now(); // Set the start time to the current time
  interval = setInterval(function() {
    // Calculate the current time based on the elapsed time
    let elapsedTime = Date.now() - startTime;
    let t = elapsedTime / 1000; // Convert elapsed time to seconds

    // Calculate the speed based on the function
    let speed = 1 + Math.floor(Math.pow(t, 2));
    // Add or subtract time based on the input value and the speed
    time += input >= speed ? speed : (input <= -speed ? -speed : input);
    input += input >= speed ? -speed : (input <= -speed ? speed : -input);
    updateTimer();

    // Check if the input value has been reached
    if (input === 0) {
      interval = clearInterval(interval);
      if (timer_caller) {timer_div.classList.remove(timer_caller)};
    }
  }, 50);

});

// Function to update the timer display
function updateTimer() {
  if (time <= 0) {
    timer_div.innerHTML = "Time's Up!";
    return
  }

  // Calculate the hours, minutes, and seconds
  let hours = Math.floor(time / (60 * 60));
  let minutes = Math.floor((time % (60 * 60)) / 60);
  let seconds = time % 60;

  // Format the time as a string
  let timerString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

  // Update the timer display
  timer_div.innerHTML = timerString;
}

// Update the timer every second
let updater = setInterval(function() {
  if (!FirstTime) {
    // Decrement the time by 1 second
    time--;
    realTime--;
    if (time <= 0) {
      time = 0;
      timer_div.classList.remove('crit_time')
      clearInterval(updater);
      eventSource.close(); // Close the EventSource when the timer reaches 0
    } else if (time < 60) {
      timer_div.classList.add('crit_time');
    } else if (realTime >= 60) {
      timer_div.classList.remove('crit_time');
    }
    // Update the timer display
    updateTimer();
  }
}, 1000);


document.addEventListener("visibilitychange", function() {
  // Get the current visibility state
  var hidden = document.hidden;

  // Check if the page is hidden
  if (!hidden && !interval && deadline > Date.now() && time ) {
    console.log("The page is visible", interval);
    let currentDate = new Date();
    time = realTime = Math.floor((deadline - currentDate) / 1000);
    console.log("The page is", deadline, currentDate, time, realTime);
  }
});