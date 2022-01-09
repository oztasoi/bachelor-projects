const express = require('express');
const request = require('request');
const router = express.Router();

router.get('/home', (req, res) => {
    return res.render('index');
});

router.post('/login-artist', (req, res) => {
    var login_body = JSON.stringify({"name" : req.body.name, "surname" : req.body.surname, "log-type" : "artist"});
    request.post('http://0.0.0.0:5001/login', {json: login_body}, function(error, response, body) {
        if(response.statusCode == 200){
            return res.render('artists');
        }
        else{
            return res.redirect('home');
        }
    })
});

router.post('/login-listener', (req, res) => {
    var login_body = JSON.stringify({"username" : req.body.username, "email" : req.body.email, "log-type" : "listener"});
    request.post('http://0.0.0.0:5001/login', {json: login_body}, function(error, response, body) {
        if(response.statusCode == 200){
            return res.render('listeners');
        }
        else{
            return res.redirect('home');
        }
    })
});

router.post('/logout', (req, res) => {
    return res.redirect('home');
});

module.exports = router;