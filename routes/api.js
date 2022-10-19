var express = require('express');
var router = express.Router();
const multer = require('multer');
const upload = multer({dest: './uploads'});
const {spawn} = require("child_process");
const Evaluation = require('../model/Evaluation');
const cors = require("cors");


/* GET home page. */
router.get('/tables', cors(), function (req, res, next) {
    Evaluation
        .find({}, {_id: 0, __v: 0, email: 0})
        .sort({sum: -1})
        .then((data) => {
            res.send(data);
        })
        .catch((err) => {
            console.error(err);
            res.sendStatus(500);
        });
});

const resultParser = upload.fields([{name: "STS_ca", maxCount: 1}, {name: "POS", maxCount: 1}, {name: "CatalanQa", maxCount: 1}, {name: "XQuAD", maxCount: 1}, {name: "TeCla", maxCount: 1}, {name: "TECa", maxCount: 1}, {name: "AnCora", maxCount: 1}])
router.post('/results', cors(), resultParser, function (req, res, next) {
    // Sacar archivos del request
    let file_1 = req.files["STS_ca"][0].path;
    let file_2 = req.files["POS"][0].path;
    let file_3 = req.files["CatalanQa"][0].path;
    let file_4 = req.files["XQuAD"][0].path;
    let file_5 = req.files["TeCla"][0].path;
    let file_6 = req.files["TECa"][0].path;
    let file_7 = req.files["AnCora"][0].path;
    let eval_results = '';
    const py_process = spawn("python", ["./engine/main.py", file_1, file_2, file_3, file_4, file_5, file_6, file_7]);
    py_process.stdout.on('data', (data) => {
        eval_results += data;
    });

    py_process.stderr.on('data', (data) => {
        console.log(data.toString())
    })

    py_process.on('exit', (code) => {
        if (code == null || code !== 0) {
            console.error("Error with python child process. Error code was " + code);
            res.sendStatus(500);
        } else {
            const regex = /\{.*\}/g
            const result = regex.exec(eval_results)[0]
            // console.log(result);

            eval_results = JSON.parse(result);
            (new Evaluation(Object.assign(req.body, eval_results)))
                .save()
                .then(()=>{
                    res.send({ok: true});
                })
                .catch((err)=>{
                    console.error(err);
                    res.sendStatus(500);
                })
        }

    });
});

module.exports = router;
