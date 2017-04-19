var path = require('path');
var fs = require('fs');
var PythonShell = require('python-shell');

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
            args: [query['first'].split(' ').join('_'), query['second'].split(' ').join('_')]
        };
        PythonShell.run('wordnet.py', options, function(err, results) {
            if (err) throw err;
            console.log('results: %j', results);
            res.send(results[0]);
        });
    });

    app.get('*', function(req, res) {
        res.sendFile(path.resolve('public/index.html')); // load the single view file (angular will handle the page changes on the front-end)
    });
};
