var mongoInit = require('.');
var express = require('express');
var cors = require('cors')
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const indexRouter = require("./routes/api");
const helmet = require('helmet');
const basicAuth = require('express-basic-auth');
const rateLimit = require('express-rate-limit');

module.exports = ()=>{
    return mongoInit().then(()=>{
    //return (()=>{
        var app = express();
        app.use(helmet());
        app.use(logger('dev'));
        app.use(express.json());
        app.use(express.urlencoded({extended: false}));
        app.use(cookieParser());
        app.use(cors({
            origin: '*'
        }));
        app.use(rateLimit({
                windowMs: 15 * 60 * 1000, // 15 minutes
                max: 50, // Limit each IP to 100 requests per `window` (here, per 15 minutes)
                standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
                legacyHeaders: false, // Disable the `X-RateLimit-*` headers
        }));
        // app.use(basicAuth({
            // authorizer: (username, password, cb) => {
                // const userMatches = basicAuth.safeCompare(username, process.env.API_USERNAME);
                // const passwordMatches = basicAuth.safeCompare(password, process.env.API_PASSWORD);
                // if (userMacthes & passwordMatches)
                    // return cb(null, true)
                // else
                    // return cb(null, false)
            // },
            // authorizeAsync: true,
        // }));
        app.use(express.static(path.join(__dirname, 'public')));
        app.use('/api', indexRouter);
        return Promise.resolve(app);
    })

}
