import React from 'react';
import {render} from 'react-dom';
const uuidv4 = require('uuid/v4');


const visitorSlug = uuidv4();
const xhttp = new XMLHttpRequest();


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
          <button id="informtiveButton" ref="startButton">Informative</button>
      </div>
    )
  }
}


class App extends React.Component {

  constructor(props, context) {
    super(props, context);
  }

  componentWillMount () {
    this.startPollingEvent();
  }

  componentWillUnmount() {
    clearTimeout(this.timeout);
  }

  startPollingEvent () {
    this.timeout = setTimeout(() => {
      xhttp.open("GET", "api/v1/event/" + visitorSlug, true);
      xhttp.send();
      console.log(xhttp.responseText);
      this.startPollingEvent();
    }, 500);
  }


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
