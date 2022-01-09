const exp = require('express'); // express foro routing.
const njk =  require('nunjucks'); // template engine
const path = require('path'); // get path object

//// Initializations
const app = exp(); // initializing the app

//// settings

app.set('port', process.env.PORT || 3000); // setting the port for current local machine

app.set('views', path.join(__dirname, 'views')); // setting views path for view engine

// setting nunjucks to configure html files, options are declared
njk.configure('views', {
    autoescape: true,
    cache: false,
    express: app
});

// setting view engine extension as .html
app.set('view engine', 'html');

app.use(exp.urlencoded({extended:false}));

// routes
app.use(require('./routes/index'));
app.use(require('./routes/login'));
app.use(require('./routes/listeners'));
app.use(require('./routes/artists'));

// server listens to
app.listen(app.get('port'), () => {
    console.log('Server on port', app.get('port'));
});