var deadline;
var timeLeft;
var FirstTime = true
hidden = document.getElementById("timer").hidden
var eventSource = new EventSource("/sse")
window.onbeforeunload = function() {
  console.log("Closing SSE connection");
  eventSource.close();
}
    function getTimeLeft(timeLeft, option = false) {
    hours = Math.floor((timeLeft)/3600)
    minutes = Math.floor((timeLeft-hours*3600)/60)
    seconds = Math.floor(timeLeft-hours*3600-minutes*60)
    minutes = minutes < 10 ? "0" + minutes : minutes
    seconds = seconds < 10 ? "0" + seconds : seconds
    return option ? {hours: parseInt(hours), minutes: parseInt(minutes), seconds: parseInt(seconds)} : {hours, minutes, seconds} 
  }
  function removeColor(className, color) {
    ["hours", "minutes", "seconds"].forEach( (element) => {
        document.getElementById(`${element}_div`).classList.remove(className)
      })
    }

  function updateTimeDivs (timeLeft) {
      var {hours, minutes, seconds} = getTimeLeft(timeLeft)
      document.getElementById("hours_div").innerHTML = hours
      document.getElementById("minutes_div").innerHTML = minutes
      document.getElementById("seconds_div").innerHTML = seconds
  }

  var addedTime = 0;
  var time = 0;
  eventSource.addEventListener("deadline", function(e) {
    console.log(JSON.parse(e.data))
    deadline = JSON.parse(e.data).deadline
    time = time ? time : deadline - Math.floor(Date.now()/1000)
    oldTimeLeft = timeLeft ? timeLeft : deadline - Math.floor(Date.now()/1000)
    timeLeft = deadline - Math.floor(Date.now()/1000)
    var {hours, minutes, seconds} = getTimeLeft(timeLeft)
    if (!FirstTime && !hidden) {
      // updateTimeDivs(timeLeft);
      addedTime = timeLeft - oldTimeLeft;
      console.log(oldTimeLeft, timeLeft, addedTime);
      let startTime = Date.now(); // Set the start time to the current time

        // Get the input value and add it to the time slowly with an animation
        let input = addedTime;
        let interval = setInterval(function() {
        // Calculate the current time based on the elapsed time
        let elapsedTime = Date.now() - startTime;
        let t = elapsedTime / 1000; // Convert elapsed time to seconds

        // Calculate the speed based on the function
        let speed = 1 + Math.floor(Math.pow(t, 2));

        // Add or subtract time based on the input value and the speed
        time += input >= speed ? speed : (input <= -speed ? -speed : input);
        input += input >= speed ? -speed : (input <= -speed ? speed : -input);
        addedTime = input;
        updateTimeDivs(time);

        // Check if the input value has been reached
        if (input === 0) {
          ["hours", "minutes", "seconds"].forEach( (element) => {
            document.getElementById(`${element}_div`).classList.remove("added_time", "subbed_time")
          });
          clearInterval(interval);
        }
      }, 50);
      if (addedTime > 0) {
        
      ["hours", "minutes", "seconds"].forEach( (element) => {
        document.getElementById(`${element}_div`).classList.add("added_time")
      });
      // setTimeout(removeColor, 1000, 'added_time', 'green');
        } else {
            ["hours", "minutes", "seconds"].forEach( (element) => {
            document.getElementById(`${element}_div`).classList.add("subbed_time")
        });
        setTimeout(removeColor, 1000, 'subbed_time', 'yellow');
            }
    } else {
      FirstTime = false
    }
    console.log(hours, minutes, seconds)
    console.log("update!")
  }, false)

  eventSource.addEventListener("message", function(e) {
    console.log(e.data)
  }, true)

  // window.onload = function() {
  //   timeLeft = deadline - Math.floor(Date.now()/1000)
  // }
  var animated = false
  setInterval(() => {
    if (!animated) {
      timeLeft = deadline - Math.floor(Date.now()/1000)
      if(time >= 0) {
        updateTimeDivs(time)
        if (time < 60) {
          ["hours", "minutes", "seconds"].forEach( (element) => {
            document.getElementById(`${element}_div`).classList.add("last_time")
          })
          setTimeout(removeColor, 500, 'last_time', 'red')
        }
        time--;
      } else if (!hidden) {
        // hidden = document.getElementById("timer").hidden = true;
        // document.getElementById("time_up").hidden = false;
        hidden = true
        document.getElementById("hours_div").innerHTML = "0:"
        document.getElementById("minutes_div").innerHTML = "00:"
        document.getElementById("seconds_div").innerHTML = "00"
      }
    } 
  }, 1000);

  const xhr = new XMLHttpRequest();

xhr.open('POST', '/subathon_settings');
xhr.setRequestHeader('Content-Type', 'application/json');

xhr.onreadystatechange = function() {
  if (xhr.readyState === 4 && xhr.status === 200) {
    // Do something with the response
  }
};

xhr.send(JSON.stringify({
  message: 'Hello, World!'
}));


