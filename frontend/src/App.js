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
const GigSidebarArtist = (props, context) => {
  var artist = {}
  if(props.artist != null){
    artist = props.artist
  }
  const artistTrack = artist.artistLinks ;
  var trackExists = false ;
  var track = null ;
  if(artistTrack !== undefined){
    trackExists = true
    track = artistTrack.bandcamp
  }
  return(
    <div className="artistListing">
      <span className="artistName">{artist.artistName}</span>
      <button onClick={(e) => props.playNextTrack(BandcampTrack(track))} className="artistTrack"><i className="fa fa-play"></i></button>
    </div>
  )
}
;

//returns the bandcamp embedded object
const BandcampTrack = (bandcampTrack) => {
  if(bandcampTrack === undefined){
    return(null)
  }
  const track = bandcampTrack.bandcampTracks[0]
  const srcString = "https://bandcamp.com/EmbeddedPlayer/" + track.type + "=" + track.id + "/size=small/bgcol=333333/linkcol=ffffff/transparent=true/"
  return(
   <iframe style="border: 0; width: 100%; height: 42px;" src={srcString} seamless><a href={track.link}>Joonya Spirit by Jaala</a></iframe>
  );
}
;

const GigSidebarItem = (props, context) => {
  //console.log(props.gig);
  //console.log(props.artist) ;
  //console.log(props.venue) ;
  var venue = {}
  var artist = []
  if (props.venue != null){
    venue = props.venue
  }
  if(props.artist != null){
    artist = props.artist
  }
  return(
    <div className="gigInfo">
      <div className="gigInfoMain">
        <span className="venueName">{venue.venueName}</span>
        <span className="gigTime">{props.gig.gigDatetime}</span>
        <span className="gigPrice">{props.gig.gigPrice}</span>
      </div>
      <div className="gigInfoArtist">
        {artist.map(x => <GigSidebarArtist key={(x || {}).artistId} artist={x} playNextTrack={props.playNextTrack} />)}
      </div>
    </div>
  )
}
;


export class GigSidebar extends Component {
  render(){
    //console.log(this.props.gig) ;
    var gigArtist = {} ;
    var gigVenue = {} ;
    for (var i = 0; i < this.props.gig.length; i++) {
      var g = this.props.gig[i] ;
      var artist = g.headlineArtist.map(ha => this.props.artist[ha])
      artist = artist.concat(g.supportArtist.map(ha => this.props.artist[ha])) ;
      gigArtist[g.gigId] = artist ;
      gigVenue[g.gigId] = this.props.venue[g.venueId] ;
    }
    //console.log(this.props.artist) ;
    //console.log(gigArtist) ;
    //console.log(gigVenue) ;
    return(
      <section className="gigSidebar">
        <div id="gigSidebarList">
          {this.props.gig.map(x => <GigSidebarItem key={x.gigId} gig={x} artist={gigArtist[x.gigId]} venue={gigVenue[x.gigId]} playNextTrack={this.props.playNextTrack}/> )}
        </div>
      </section>
    )
  }
}
;

//map
//shows all gigs in area that fit criteria, when one is clicked it is highlighted on both

//music player
//contains queue of tracks to play
//when a new track comes in change the track playing
export class MusicPlayer extends Component {
  render(){
    console.log(this.props.nextTrack)
    return(
      this.props.nextTrack
    )
  }
}
;


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
    this.playNextTrack = this.playNextTrack.bind(this);
    this.state = {
      gig:[],
      venueId:[],
      venue:[],
      artistId:[],
      artist:[],
      nextTrack:null
    }
  }
  setGig(gig){
    var venueId = gig.map(x => x.venueId)
    venueId =  Array.from(new Set(venueId))
    var artistId = gig.map(x => x.headlineArtist.concat(x.supportArtist))
    artistId = Array.from(new Set(artistId));
    //artistId = artistId.flat();
    artistId = [].concat.apply([], artistId)
    this.setState({
      gig:gig,
      venueId:venueId,
      artistId:artistId
    })
  }
  setVenue(venue){
    var venueObject = {} ;
    for (var i = 0; i < venue.length; i++) {
      var thisVenue = venue[i] ;
      venueObject[thisVenue.venueId] = thisVenue
    }
    this.setState({
      venue:venueObject
    })
  }
  setArtist(artist){
    var artistObject = {} ;
    for (var i = 0; i < artist.length; i++) {
      var thisArtist = artist[i] ;
      artistObject[thisArtist.artistId] = thisArtist
    }
    //console.log(artistObject) ;
    this.setState({
      artist:artistObject
    })
  }
  playNextTrack(nextTrack){
    this.setState({
      nextTrack:nextTrack
    })
  }
  render() {
    var startDate = "2018-07-21" ;
    var endDate = "2018-07-21" ;
    return(
      <div>
        <GetGig startDate={startDate} endDate={endDate} setGig={this.setGig} />
        <GetVenue venueId={this.state.venueId} setVenue={this.setVenue} />
        <GetArtist artistId={this.state.artistId} setArtist={this.setArtist} />
        <MusicPlayer nextTrack={this.state.nextTrack} />
        <GigSidebar gig={this.state.gig} artist={this.state.artist} venue={this.state.venue} playNextTrack={this.playNextTrack}/>
      </div>
    )
  }
}
;
