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

// add query functions
// function to get all objects
function getGig(req,res,next){
  var formatTs = getRunTimestamp(req);
  dbConnection.any("select $1", req.params.startTime)
    .then(function(data){
      res.status(200)
        .json({
          status:"success",
          data:data,
          message:"Retrieved all channels"
        });
    })
    .catch(function(err){
      return next(err);
    });
}
;

module.exports = {
	getGig:getGid
}
;