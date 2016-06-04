var fs = require('fs'),
	readline = require('readline'),
	Utf = require('./utf.js'),
	utf_obj = new Utf();

var rd = readline.createInterface({
	input: fs.createReadStream(process.argv[2]),
});

rd.on('line', function(line) {
	console.log(utf_obj.URLdecode(line));
});
