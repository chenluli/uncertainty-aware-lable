function Observer() {
    var observer = {};
    var viewList = [];
	observer.mintime=1364774400;
	observer.starttime=1365078600;//1365325500;//1365078600;
	observer.ip2int=function(ip){
		var num = 0;
		//console.log(ip);
		ip = ip.split(".");
		num = Number(ip[0]) * 256 * 256 * 256 + Number(ip[1]) * 256 * 256 + Number(ip[2]) * 256 + Number(ip[3]);
		num = num >>> 0;
		return num;
	}
	observer.int2iP=function(num){
		var str;
		var tt = new Array();
		tt[0] = (num >>> 24) >>> 0;
		tt[1] = ((num << 8) >>> 24) >>> 0;
		tt[2] = (num << 16) >>> 24;
		tt[3] = (num << 24) >>> 24;
		str = String(tt[0]) + "." + String(tt[1]) + "." + String(tt[2]) + "." + String(tt[3]);
		return str;
	}
	observer.inttime2str=function(num){
		var str;
		var t = new Date(num*1000-8*60*60*1000)
		str=t.getFullYear()+"-"+t.getDate()+"-"+t.getDay()+" "+t.getHours()+":"+t.getMinutes();
		return str;
	}
    observer.addView = function(view) {
        viewList.push(view);
    }
    observer.fireEvent = function(message, data, from) {
        viewList.forEach(function(view) {
            if (view.hasOwnProperty('onMessage')) {
                view.onMessage(message, data, from);
            }

        })
    }
    return observer;
}




var obs = Observer();
var timeline = Timeline(obs);
var soinn = Soinn(obs);
var statistic = Statistic(obs);
var netforce = Netforce(obs);
var line = Line(obs);
var matrix = Matrix(obs);
