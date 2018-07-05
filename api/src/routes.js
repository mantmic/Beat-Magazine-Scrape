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
  //post artists
  app.route('/artist/push/:artistId')
	.post(db.pushArtist)
  //post venues
};