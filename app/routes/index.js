var path = require('path');
var fs = require('fs');
var PythonShell = require('python-shell');
var jsonfile = require('jsonfile');

module.exports = function(app) {
    app.get('/api/getList', function(req, res) {
        var allArray = [],
            aArray = [],
            pArray = [];
        fs.readFile(path.resolve('data/' + 'animals.txt'), function(err, data) {
            if (err) throw err;
            aArray = data.toString().split("\n");
            fs.readFile(path.resolve('data/' + 'plants.txt'), function(err, data) {
                if (err) throw err;
                pArray = data.toString().split("\n");
                allArray = aArray.concat(pArray);
                res.send(JSON.stringify(allArray));
            });
        });
    });

    app.get('/api/getParas', function(req, res) {
        var query = req.query;
        console.log(query['first'].split(' ').join('_'));
        console.log(query['second'].split(' ').join('_'));
        var options = {
            mode: 'json',
            scriptPath: 'scripts/',
            pythonPath: '/usr/bin/python3',
            args: [query['first'].split(' ').join('_'), query['second'].split(' ').join('_')]
        };
        PythonShell.run('wordnet.py', options, function(err, results) {
            if (err) throw err;
            // console.log('results: %j', results);
            res.send(results[0]);
        });
    });

    app.post('/api/addPair', function(req, res) {
        var query = req.query;
        query.entity1 = query.entity1.split(' ').join('_');
        query.entity2 = query.entity2.split(' ').join('_');
        var filename = "";
        if (query.entity1.localeCompare(query.entity2) < 0) {
            filename = query.entity1 + "_" + query.entity2;
        } else {
            filename = query.entity2 + "_" + query.entity1;
        }
        var pathname = 'data/pairs/' + filename + '.json';
        jsonfile.readFile(pathname, function(err, data) {
            if (err) {
		console.log(pathname, filename);
                fs.writeFileSync(pathname, JSON.stringify({}), function(error) {
                    if (error) {
                        console.log(error);
                    }
                });
                console.log("The file was saved!");
                data = {};
            }
            // obj = JSON.parse(data);
            obj = data;
            if (obj.hasOwnProperty('sentences')) {
                var sentencePair = {};
                sentencePair['heading1'] = query.heading1;
                sentencePair['heading2'] = query.heading2;
                sentencePair['sentence1'] = query.sentence1;
                sentencePair['sentence2'] = query.sentence2;
                obj['sentences'].push(sentencePair);
                jsonfile.writeFile(pathname, obj, function(err) {
                    console.error(err);
                });
            } else {
                var temp = {};
                temp['entity1'] = query.entity1;
                temp['entity2'] = query.entity2;
                temp['comparable'] = 0;
                temp['sentences'] = [];
                var sentencePair = {};
                sentencePair['heading1'] = query.heading1;
                sentencePair['heading2'] = query.heading2;
                sentencePair['sentence1'] = query.sentence1;
                sentencePair['sentence2'] = query.sentence2;
                temp['sentences'].push(sentencePair);
                jsonfile.writeFile(pathname, temp, function(err) {
                    console.error(err);
                });
            }
        });
    });

    app.post('/api/updateComparable', function(req, res) {
        var query = req.query;
        query.entity1 = query.entity1.split(' ').join('_');
        query.entity2 = query.entity2.split(' ').join('_');
        var filename = "";
        if (query.entity1.localeCompare(query.entity2) < 0) {
            filename = query.entity1 + "_" + query.entity2;
        } else {
            filename = query.entity2 + "_" + query.entity1;
        }
        console.log(filename);
        var pathname = 'data/pairs/' + filename + '.json';
        jsonfile.readFile(pathname, function(err, data) {
            if (err) {
                console.log(err);
                fs.writeFileSync(pathname, JSON.stringify({}), function(error) {
                    if (error) {
                        console.log(error);
                    }
                });
                console.log("The file was saved!");
                data = {};
            }
            console.log(data);
            // obj = JSON.parse(data);
            obj = data;
            if (obj.hasOwnProperty('comparable')) {
                if (query.comparable == '0') {
                    obj.comparable = obj.comparable - 1;
                } else {
                    obj.comparable = obj.comparable + 1;
                }
                jsonfile.writeFile(pathname, obj, function(err) {
                    console.error(err);
                });
            } else {
                var temp = {};
                temp['entity1'] = query.entity1;
                temp['entity2'] = query.entity2;
                if (query.comparable == '0') {
                    temp['comparable'] = -1;
                } else {
                    temp['comparable'] = 1;
                }
                temp['sentences'] = [];
                jsonfile.writeFile(pathname, temp, function(err) {
                    console.error(err);
                });
            }
        });
    });

    app.get('*', function(req, res) {
        res.sendFile(path.resolve('public/index.html')); // load the single view file (angular will handle the page changes on the front-end)
    });
};
