import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';

const apiUrl = 'https://beat-magazine-map.herokuapp.com/' ;


export class GetGig extends React.Component {
  constructor(props) {
    super(props);
    this.setGig = this.setGig.bind(this);
  }
  setGig(gig){
    this.props.setGig(gig)
  }
  //dont get gigs if the start and end date are the same
  shouldComponentUpdate(nextProps){
   //check if the props have changed
   return this.props.startDate !== nextProps.startDate || this.props.endDate !== nextProps.endDate
    //return nextProps.startTime !== this.props.startTime || nextProps.endtime !== this.props.endTime || nextProps.nicChannelId.sort().join(',') !== this.props.nicChannelId.sort().join(',')
 }
  render() {
    fetch(apiUrl + 'gig?startDate=' + this.props.startDate + '&endDate=' + this.props.endDate,{ //url query string asks for just one quote
      method: 'get',
    }).then((response) => response.json())
      .then((responseData) => {
        this.setGig(responseData.data) ;
    })
    return (
      null
    );
  }
}
;

export class GetVenue extends React.Component {
  constructor(props) {
    super(props);
    this.setVenue = this.setVenue.bind(this);
  }
  setVenue(venue){
    this.props.setVenue(venue)
  }
  //dont get gigs if the start and end date are the same
  shouldComponentUpdate(nextProps){
   //check if the props have changed
   return this.props.venueId !== nextProps.venueId
    //return nextProps.startTime !== this.props.startTime || nextProps.endtime !== this.props.endTime || nextProps.nicChannelId.sort().join(',') !== this.props.nicChannelId.sort().join(',')
 }
  render() {
    fetch(apiUrl + 'venue',{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "venueId":this.props.venueId
      })
    })
    .then((response) => response.json())
    .then((responseData) => {
        this.setVenue(responseData.data) ;
    })
    return (
      null
    );
  }
}
;

export class GetArtist extends React.Component {
  constructor(props) {
    super(props);
    this.setArtist = this.setArtist.bind(this);
  }
  setArtist(artist){
    this.props.setArtist(artist)
  }
  //dont get gigs if the start and end date are the same
  shouldComponentUpdate(nextProps){
   //check if the props have changed
   return this.props.artistId !== nextProps.artistId
 }
  render() {
    fetch(apiUrl + 'artist',{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "artistId":this.props.artistId
      })
    })
    .then((response) => response.json())
    .then((responseData) => {
        this.setArtist(responseData.data) ;
    })
    return (
      null
    );
  }
}
;

//sidebar
//shows all gigs that fit criteria, when one is clicked it is highlighted on both

//map
//shows all gigs in area that fit criteria, when one is clicked it is highlighted on both

//music player
//contains queue of tracks to play
//when a new track comes in change the track playing

//app variables
//all gigs that fit criteria
//all artists that are related to those gigs
//all venues that are related to those gigs
//the selected gig (to show on both map and sidebar)
export class App extends Component {
  constructor(props) {
    super(props);
    this.setGig = this.setGig.bind(this);
    this.setVenue = this.setVenue.bind(this);
    this.setArtist = this.setArtist.bind(this);
    this.state = {
      gig:[],
      venueId:[],
      venue:[],
      artistId:[],
      artist:[]
    }
  }
  setGig(gig){
    console.log(gig)
    var venueId = gig.map(x => x.venueId)
    venueId =  Array.from(new Set(venueId))
    var artistId = gig.map(x => x.headlineArtist.concat(x.supportArtist))
    artistId = Array.from(new Set(artistId));
    //artistId = artistId.flat();
    artistId = [].concat.apply([], artistId)
    console.log(artistId)
    this.setState({
      gig:gig,
      venueId:venueId,
      artistId:artistId
    })
  }
  setVenue(venue){
    console.log(venue)
    this.setState({
      venue:venue
    })
  }
  setArtist(artist){
    console.log(artist)
    this.setState({
      artist:artist
    })
  }
  render() {
    var startDate = "2018-07-01" ;
    var endDate = "2018-07-30" ;
    return(
      <div>
        <GetGig startDate={startDate} endDate={endDate} setGig={this.setGig} />
        <GetVenue venueId={this.state.venueId} setVenue={this.setVenue} />
        <GetArtist artistId={this.state.artistId} setArtist={this.setArtist} />
        <p>
          {String(this.state.gig)}
        </p>
      </div>
    )
  }
}
;
