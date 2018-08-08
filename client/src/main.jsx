import React from 'react';
import {render} from 'react-dom';


var slug = "test";

window.setSlug = function(slugValue) {
  slug = slugValue;
}

window.getSlug = function() {
  return slug;
};

class VideoBox extends React.Component {

  componentDidMount () {

    var width = 320;    // We will scale the photo width to this
    var height = 0;     // This will be computed based on the input stream

    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.

    var streaming = false;

    navigator.getMedia = ( navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);

    var video = this.refs.videoFrame;
    var canvas = this.refs.canvasBox;
    var photo = this.refs.outputImage;
    var startbutton = this.refs.startButton;

    navigator.getMedia(
      {
        video: true,
        audio: false
      },
      function(stream) {
        if (navigator.mozGetUserMedia) {
          video.mozSrcObject = stream;
          } else {
          var vendorURL = window.URL || window.webkitURL;
          video.src = vendorURL.createObjectURL(stream);
        }
        video.play();
      },
      function(err) {
        console.log("An error occured! ", err);
      }
    );

    // Fill the photo with an indication that none has been
    // captured.

    function clearphoto() {
      var context = canvas.getContext('2d');
      context.fillStyle = "#AAA";
      context.fillRect(0, 0, canvas.width, canvas.height);

      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
    }

    // Capture a photo by fetching the current contents of the video
    // and drawing it into a canvas, then converting that to a PNG
    // format data URL. By drawing it on an offscreen canvas and then
    // drawing that to the screen, we can change its size and/or apply
    // other changes before drawing it.

    function takepicture() {
      var context = canvas.getContext('2d');
      if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
        } else {
          clearphoto();
      }
    }

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);

        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.

        if (isNaN(height)) {
          height = width / (4/3);
        }

        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);

    startbutton.addEventListener('click', function(ev){
      console.log("Click!");
      takepicture();
      ev.preventDefault();
    }, false);

    clearphoto();
  }

  render () {
    return (
      <div className="contentarea">
        <h1>
          What do you see?
        </h1>
        <div className="camera">
          <video id="video" ref="videoFrame">Video stream not available.</video>
          <button id="startbutton" ref="startButton">Take photo</button>
        </div>
        <canvas id="canvas" ref="canvasBox">
        </canvas>
        <div className="output">
          <img id="photo" ref="outputImage" />
        </div>
      </div>
    )
  }
}

class App extends React.Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      locationMessage: ""
    }
  }

  componentWillMount () {
    var message = "";
    if (!this.geoLocationEnabled()) {
      message = "Geolocation is not supported by your browser";
    }

    this.setState({
      locationMessage: message
    });
  }

  geoLocationEnabled() {
    if (!navigator.geolocation){
      return false;
    }
    return true;
  }

  showPosition (position) {
    console.log(position);
    var latLongMessage = position.coords.latitude + "," + position.coords.longitude;

    var img = this.refs.mapBox;
    var apiKey = "AIzaSyCFtyhT9MpF4jVbFQCJVWIKzRmChznrKtc";
    img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + latLongMessage + "&zoom=13&size=300x300&sensor=false&key=" + apiKey;

    output.appendChild(img);
    this.setState({
      locationMessage: latLongMessage
    });
  }

  showError () {
    this.setState({
      locationMessage: "Unable to retrieve your location"
    });
  }

  geoFindMe () {
    console.log("geoFindMe");
    navigator.geolocation.getCurrentPosition(this.showPosition.bind(this), this.showError.bind(this));
  }

  render () {
    return (
      <div>
      <div>The slug is: {getSlug()}</div>
        <div id="geolocation">
          <h1>Where are you?</h1>
          <div id="mapIt">
            <p><button onClick={this.geoFindMe.bind(this)}>Show my location</button></p>
            <div id="out">{this.state.locationMessage}</div>
            <img ref="mapBox" />
          </div>
        </div>

        <VideoBox />

      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));
