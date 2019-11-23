
var bodyParser = require('body-parser');
var express = require('express');
var request = require('request');
var path = require('path');

var app = express();

app.use(express.static('views'));
app.use(bodyParser.urlencoded({ extended:true }));
app.set('view engine', 'ejs');
app.get('/', function(req,res){
    res.render('index');
});
app.listen(3000,function(){
    console.log("Connected on port 3000!");
})