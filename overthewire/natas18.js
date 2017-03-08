/*var request = require('request');
request({
	url: 'http://natas18.natas.labs.overthewire.org/index.php',
	method: 'POST',

});*/

var http = require('http');
var post_option = {
	host: 'http://natas18.natas.labs.overthewire.org',
	path: '/index.php',
	//port: '80',
	//method: 'POST',
	//headers: {
		//'PHPSESSID': 1
	//}
};
/*var post_req = http.request(post_option, function (res){
	console.log(res.statusCode);
});*/
http.post(post_option, function (res){
	console.log("OAO");
});
