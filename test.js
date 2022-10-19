var mongoInit = require('./index');
mongoInit().then(()=>{
    console.log('bien');
}).catch((err)=>{
    console.error(err);
});
