var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;
  bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//register the routes
var routes = require('./src/routes.js');
routes(app);

app.listen(port);

console.log('BEAT RESTful API server started on: ' + port);
