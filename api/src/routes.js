module.exports = function(app){
  var db = require('./queries.js');
  //get gigs for daterrange
  app.route('/gig')
    .get(db.getGig)
    .post(db.getGig)
  //get artists by ids
  app.route('/artist')
    .post(db.getArtist)
  //get venues by ids
   app.route('/venue')
    .post(db.getVenue)
  //post gigs
  app.route('/gig/push/:gigId')
	.post(db.pushGig)
  //post artists
  app.route('/artist/push/:artistId')
	.post(db.pushArtist)
  //post venues
  app.route('/venue/push/:venueId')
	.post(db.pushVenue)
};
