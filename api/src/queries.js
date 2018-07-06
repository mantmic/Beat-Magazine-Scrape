var promise = require('bluebird');
var config = require('../config.json');

var options = {
  // Initialization Options
  promiseLib: promise
};

var pgp = require('pg-promise')(options);

//load the db connection string from the config file
dbConnection = pgp(config["dbConnection"])

//post parameters = req.body.[param]
//get parameters = req.params.[param]

//function to get artists
function getArtist(req,res,next){
  dbConnection.any('select \
	artist_id 		as "artistId", \
	beat_type 		as "beatAristType", \
	artist_name 	as "artistName", \
	artist_links 	as "artistLinks", \
	artist_gigs 	as "artistGigs" \
from  \
	beat.artist  \
where artist_id = any($1)', req.body.artistId || [])
    .then(function(data){
      res.status(200)
        .json({
          status:"success",
          data:data,
          message:"Retrieved artists"
        });
    })
    .catch(function(err){
      return next(err);
    });
}
;

//function to get venues
function getVenue(req,res,next){
  dbConnection.any('select \
	venue_id 		as "venueId", \
	venue_name 		as "venueName", \
	venue_address 	as "venueAddress", \
	lat, \
	lon \
from  \
	beat.venue \
where venue_id = any($1)', req.body.venueId || [])
    .then(function(data){
      res.status(200)
        .json({
          status:"success",
          data:data,
          message:"Retrieved venues"
        });
    })
    .catch(function(err){
      return next(err);
    });
}
;

//function to get gigs
function getGig(req,res,next){
  dbConnection.any('select \
	gig_id 			as "gigId", \
	gig_datetime 	as "gigDatetime", \
	venue_id 		as "venueId", \
	gig_genre 		as "gigGenre", \
	headline_artist as "headlineArtist", \
	support_artist 	as "supportArtist", \
	gig_price		as "gigPrice" \
from \
	beat.gig_vw \
where gig_date between $1 and $2 or gig_id = any($3)', [req.params.startDate || '1970-01-01', req.params.endDate || '2199-12-31', req.body.gigId || []])
    .then(function(data){
      res.status(200)
        .json({
          status:"success",
          data:data,
          message:"Retrieved gigs"
        });
    })
    .catch(function(err){
      return next(err);
    });
}
;

//function to push artists
function pushArtist(req,res,next){
  dbConnection.any('select beat.post_artist_fnc ( \
	  p_artist_id 		:= $1 \
	, p_beat_type 		:= $2 \
	, p_artist_name 	:= $3 \
	, p_artist_links 	:= $4 )'
	, [req.params.artistId, req.body.beatArtistType, req.body.artistName, req.body.artistLinks])
    .then(function(data){
      res.status(200)
        .json({
          status:"success",
          data:data,
          message:"Pushed artist"
        });
    })
    .catch(function(err){
      return next(err);
    });
}
;

module.exports = {
	getGig:getGig,
	getArtist:getArtist,
	getVenue:getVenue,
	pushArtist:pushArtist
}
;