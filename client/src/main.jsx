import React from 'react';
import {render} from 'react-dom';
const uuidv4 = require('uuid/v4');


const visitorSlug = uuidv4();
const xhttp = new XMLHttpRequest();


// class VideoBox extends React.Component {

//   componentDidMount () {

//     var width = 320;    // We will scale the photo width to this
//     var height = 0;     // This will be computed based on the input stream

//     // |streaming| indicates whether or not we're currently streaming
//     // video from the camera. Obviously, we start at false.

//     var streaming = false;

//     navigator.getMedia = ( navigator.getUserMedia ||
//     navigator.webkitGetUserMedia ||
//     navigator.mozGetUserMedia ||
//     navigator.msGetUserMedia);

//     var video = this.refs.videoFrame;
//     var canvas = this.refs.canvasBox;
//     var photo = this.refs.outputImage;
//     var startbutton = this.refs.startButton;

//     navigator.getMedia(
//       {
//         video: true,
//         audio: false
//       },
//       function(stream) {
//         if (navigator.mozGetUserMedia) {
//           video.mozSrcObject = stream;
//           } else {
//           var vendorURL = window.URL || window.webkitURL;
//           video.src = vendorURL.createObjectURL(stream);
//         }
//         video.play();
//       },
//       function(err) {
//         console.log("An error occured! ", err);
//       }
//     );

//     // Fill the photo with an indication that none has been
//     // captured.

//     function clearphoto() {
//       var context = canvas.getContext('2d');
//       context.fillStyle = "#AAA";
//       context.fillRect(0, 0, canvas.width, canvas.height);

//       var data = canvas.toDataURL('image/png');
//       photo.setAttribute('src', data);
//     }

//     // Capture a photo by fetching the current contents of the video
//     // and drawing it into a canvas, then converting that to a PNG
//     // format data URL. By drawing it on an offscreen canvas and then
//     // drawing that to the screen, we can change its size and/or apply
//     // other changes before drawing it.

//     function takepicture() {
//       var context = canvas.getContext('2d');
//       if (width && height) {
//         canvas.width = width;
//         canvas.height = height;
//         context.drawImage(video, 0, 0, width, height);

//         var data = canvas.toDataURL('image/png');
//         photo.setAttribute('src', data);
//         } else {
//           clearphoto();
//       }
//     }

//     video.addEventListener('canplay', function(ev){
//       if (!streaming) {
//         height = video.videoHeight / (video.videoWidth/width);

//         // Firefox currently has a bug where the height can't be read from
//         // the video, so we will make assumptions if this happens.

//         if (isNaN(height)) {
//           height = width / (4/3);
//         }

//         video.setAttribute('width', width);
//         video.setAttribute('height', height);
//         canvas.setAttribute('width', width);
//         canvas.setAttribute('height', height);
//         streaming = true;
//       }
//     }, false);

//     startbutton.addEventListener('click', function(ev){
//       console.log("Click!");
//       takepicture();
//       ev.preventDefault();
//     }, false);

//     clearphoto();
//   }

//   render () {
//     return (
//       <div className="contentarea">
//         <h1>
//           What do you see?
//         </h1>
//         <div className="camera">
//           <video id="video" ref="videoFrame">Video stream not available.</video>
//           <button id="startbutton" ref="startButton">Take photo</button>
//         </div>
//         <canvas id="canvas" ref="canvasBox">
//         </canvas>
//         <div className="output">
//           <img id="photo" ref="outputImage" />
//         </div>
//       </div>
//     )
//   }
// }


class InformativeButton extends React.Component {

  componentDidMount () {
    informtiveButton.addEventListener('click', function(ev){
      console.log("Interesting!");
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "api/v1/event/informative/" + visitorSlug, true);
      xhr.send();
      ev.preventDefault();
    }, false);
  }

  render () {
    return (
      <div>
          <button id="informtiveButton" ref="startButton">Take photo</button>
      </div>
    )
  }
}


class App extends React.Component {

  constructor(props, context) {
    super(props, context);
    // this.state = {
    //   locationMessage: ""
    // }
  }

  componentWillMount () {
    this.startPollingEvent();
  }

  componentWillUnmount() {
    clearTimeout(this.timeout);
  }

  // geoLocationEnabled() {
  //   if (!navigator.geolocation){
  //     return false;
  //   }
  //   return true;
  // }

  // showPosition (position) {
  //   console.log(position);
  //   var latLongMessage = position.coords.latitude + "," + position.coords.longitude;

  //   var img = this.refs.mapBox;
  //   var apiKey = "AIzaSyCFtyhT9MpF4jVbFQCJVWIKzRmChznrKtc";
  //   img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + latLongMessage + "&zoom=13&size=300x300&sensor=false&key=" + apiKey;

  //   output.appendChild(img);
  //   this.setState({
  //     locationMessage: latLongMessage
  //   });
  // }

  // showError () {
  //   this.setState({
  //     locationMessage: "Unable to retrieve your location"
  //   });
  // }

  // geoFindMe () {
  //   console.log("geoFindMe");
  //   navigator.geolocation.getCurrentPosition(this.showPosition.bind(this), this.showError.bind(this));
  // }

  startPollingEvent () {
    this.timeout = setTimeout(() => {
      xhttp.open("GET", "api/v1/event/" + visitorSlug, true);
      xhttp.send();
      console.log(xhttp.responseText);
      this.startPollingEvent();
    }, 500);
  }

  // render () {
  //   return (
  //     <div>
  //     <div>The slug is: {visitorSlug}</div>
  //       <div id="geolocation">
  //         <h1>Where are you?</h1>
  //         <div id="mapIt">
  //           <p><button onClick={this.geoFindMe.bind(this)}>Show my location</button></p>
  //           <div id="out">{this.state.locationMessage}</div>
  //           <img ref="mapBox" />
  //         </div>
  //       </div>

  //       <VideoBox />

  //     </div>
  //   );
  // }

  render () {
    return (
      <div>
        <p>
          <b>Malaysia Airlines Flight 370</b> was a scheduled international passenger flight operated by
          <a href="/wiki/Malaysia_Airlines" title="Malaysia Airlines">Malaysia Airlines</a>that disappeared on 8 March 2014 while flying from
          <a href="/wiki/Kuala_Lumpur_International_Airport" title="Kuala Lumpur International Airport">Kuala Lumpur International Airport</a>,
          Malaysia, to its destination, <a href="/wiki/Beijing_Capital_International_Airport" title="Beijing Capital International Airport">Beijing Capital International Airport</a>
          in China. Commonly referred to as "MH370", "Flight 370" or "Flight MH370", the flight was also marketed as
          <a href="/wiki/China_Southern_Airlines" title="China Southern Airlines">China Southern Airlines</a>
          Flight 748 (CZ748/CSN748) through a <a href="/wiki/Codeshare_agreement" title="Codeshare agreement">codeshare</a>,
          The crew of the <a href="/wiki/Boeing_777" title="Boeing 777">Boeing 777-200ER</a> aircraft last made contact with
          <a href="/wiki/Air_traffic_control" title="Air traffic control">air traffic control</a> around 38 minutes after takeoff
          when the flight was over the <a href="/wiki/South_China_Sea" title="South China Sea">South China Sea</a>.
          The aircraft was lost from ATC radar screens minutes later, but was tracked by military radar for another hour,
          deviating westwards from its planned flight path, crossing the <a href="/wiki/Malay_Peninsula" title="Malay Peninsula">Malay Peninsula</a>
          and <a href="/wiki/Andaman_Sea" title="Andaman Sea">Andaman Sea</a>, where it vanished 200 nautical miles (370 km) northwest of
          <a href="/wiki/Penang_Island" title="Penang Island">Penang Island</a> in northwestern Malaysia.
        </p>
        <hr></hr>

        <InformativeButton />

      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));
