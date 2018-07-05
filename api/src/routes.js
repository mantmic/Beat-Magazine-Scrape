module.exports = function(app){
  var db = require('./queries.js');
  //get gigs for daterrange
  app.route('/gig')
    .get(db.getGig)
  //get artists by ids
  //get venues by ids 
  //post gigs 
  //post artists 
  //post venues
};