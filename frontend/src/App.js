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
  render() {
    console.log("getting gig") ;
    fetch(apiUrl + 'gig',{ //url query string asks for just one quote
      method: 'get',
    }).then((response) => response.json())
      .then((responseData) => {
        console.log(responseData) ;
        this.setGig(responseData) ;
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
    this.state = {
      gig:[]
    }
  }
  setGig(gig){
    this.setState({
      gig:gig
    })
  }
  render() {
    //var startDate = "2018-07-01" ;
    //var endDate = "2018-07-30" ;
    //var gig = <GetGig /> ;
    return(
      <div>
        <GetGig />
        <p>
          {this.state.gig}
        </p>
      </div>
    )
  }
}
;
