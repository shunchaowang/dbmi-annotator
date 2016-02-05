module.exports = function(app, passport) {

    // INDEX PAGE ===============================
    app.get('/', function(req, res) {
        res.render('index.ejs', { message: req.flash('loginMessage') }); 
    });
    
    // LOGIN ===============================
    app.get('/login', function(req, res) {
        // render the page and pass in any flash data if it exists
        res.render('login.ejs', { message: req.flash('loginMessage') }); 
    });

    app.post('/login', passport.authenticate('local-login', {
        successRedirect : '/main', 
        failureRedirect : '/login', 
        failureFlash : true 
    }));    

    // SIGNUP ==============================
    app.get('/register', function(req, res) {
        res.render('register.ejs', { message: req.flash('signupMessage') });
    });

    app.post('/register', isRegisterFormValid, passport.authenticate('local-signup', {
	    successRedirect : '/main', 
	    failureRedirect : '/register', 
	    failureFlash : true
    })
	    );
    
    // MAIN ==============================
    app.get('/main', isLoggedIn, function(req, res) {
	var request = require("request");
	var url = "http://127.0.0.1:5000/search?email=" + req.user.email;
	
	request({url: url, json: true}, function(error,response,body){
	    if (!error && response.statusCode === 200) {
		
		res.render('main.ejs', {
		    user : req.user,
		    annotations : body,
		    message: req.flash('exportMessage')
		});
		
	    } else {
		res.render('main.ejs', {
		    user : req.user,
		    annotations : {'total':0},
		    message: req.flash('exportMessage')
		});

	    }

	    
	});
	

    });

    // LOGOUT ==============================
    app.get('/logout', function(req, res) {
        req.logout();
        res.redirect('/');
    });

    // DISPLAY ==============================
    app.get('/displayWebPage', isLoggedIn, function(req, res) {
	
	var sourceUrl = req.query.sourceURL.trim();
	var email = req.query.email;
	if (sourceUrl.indexOf('.html') >= 0){
	    res.render('displayWebPage.ejs');
	} 
	else if (sourceUrl.indexOf('.pdf') >= 0){
	    res.redirect("http://localhost:3000/viewer.html?file=" + sourceUrl+"&email=" + email);
	}
	else {
	    res.redirect('/main');
	}
	
    });


    // EXPORT ==============================
    app.get('/exportcsv', isLoggedIn, function(req, res){
	
	var filename = req.query.filename;
	
	console.log(filename);
	
	if (filename) {
	    var filepath = 'export/' + filename;
	    var request = require("request");
	    
	    var url = "http://127.0.0.1:5000/search?email=" + req.query.email;
	    
	    request({url: url, json: true}, function(error,response,body){
		if (!error && response.statusCode === 200) {
		    console.log(body);
		    
		    var json2csv = require('json2csv');
		    json2csv({data: body.rows, fields: ['email', 'rawurl', 'annotationType', 'assertion_type', 'quote', 'Drug1', 'Type1', 'Role1', 'Drug2', 'Type2', 'Role2', 'Modality', 'Evidence_modality']}, function(err, csv) {
			if (err) console.log(err);
			fs.writeFile(filepath , csv, function(err) {
			    if (err) throw err;
			    console.log('[INFO] annotation saved in export!');
			});
		    });
		    
		} else {
		    req.flash('exportMessage', 'exported failed, annotation fetch exception, please see logs or contact Yifan at yin2@pitt.edu!');
		    res.redirect('/main');

		}	
	    });
	    
	    req.flash('exportMessage', 'successfully exported!');
	    res.redirect('/main');
	    
	} else {
	    req.flash('exportMessage', 'exported failed, file not exists!');
	    res.redirect('/main');
	}	
    });

    
};

// FUNCTIONS ==============================
    
// route middleware to make sure a user is logged in
function isLoggedIn(req, res, next) {

    // if user is authenticated in the session, carry on 
    if (req.isAuthenticated())
        return next();

    // if they aren't redirect them to the home page
    res.redirect('/');
}

// validate inputs in register form
function isRegisterFormValid(req, res, next){

    req.assert('email', 'Email is not valid').isEmail();
    req.assert('username', 'Username must be at least 4 characters long').len(4);
    req.assert('password', 'Password must be at least 6 characters long').len(6);
    req.assert('repassword', 'Passwords do not match').equals(req.body.password);
    
    var errors = req.validationErrors();
    
    if (errors) {
	
	res.render('register', { 
	    title: 'Register Form Validation',
	    message: '',
	    errors: errors
        });
	
    } else {
	return next();
    } 

}

