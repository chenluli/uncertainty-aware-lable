
function Line(Observer){
	var line={};
	var opts = {            
            lines: 8, 
            length: 10, 
            width: 10,
            radius: 15, 
            corners: 1, 
            rotate: 0, 
            direction: 1, 
            color: '#d2d2d2', 
			opacity: 0.8,
            speed: 1, 
            trail: 60, 
            shadow: false, 
            hwaccel: false,          
            className: 'spinner', 
            zIndex: 2e9,
            top: '50%',
            left: '50%'
        };
	var spinner = new Spinner(opts);
	 
	//$("#view1_wait").hide();
	$("#view1_wait").show(function(){
		var target= document.getElementById('view1_wait');
		spinner.spin(target);  
	});
	
	var $brtDiv=$("#top-left-div");
    var width=$brtDiv.width();
    var height=$brtDiv.height();
	
	var leftw=10;
	var rightw=30;
	var upperheight=5;
	var bottomheight=5;
	var innerheight=10;
	
	var lineheight=90;
	var textheight=18;
	var yaxisw=30;
	var xaxish=15;
	
	var linewidth=width-leftw-rightw-yaxisw;
	var totallineheight=textheight+lineheight+xaxish;
	var linenum=0;
	
	var svg=d3.select("#view1")
			.append("svg")
			.attr("width", width)
			.attr("height", height);
	
	var curtime=Observer.starttime;
	var entropydata;//srcip dstip dstport
	var ipimportant=[];
	var ipimportant_type=[];
	var ipimportant_data=[];
	var ipselected=[];
	var ipselected_type=[];
	var ipselected_data=[];
	
	var hliparr=[];
	
	var entropycolor=["#F48061","#56A4C9","#50890E"]
	var srccolor="#AFC0DD";
	var dstcolor="#F6E3BE";
	
	var sum = function(x,y){ return x+y;};　　//求和函数
	var square = function(x){ return x*x;};　　//数组中每个元素求它的平方
	
	var x = d3.scaleTime().range([0, linewidth]);
	var timer=null;
	
	changetime();
	
	function drawgraph(){
		
		$("#view1_wait").hide();
		linenum=1+ipimportant.length+ipselected.length;
		height=upperheight+innerheight*(linenum-1)+bottomheight+totallineheight*linenum;
		svg.attr("height", height);
		
		x.domain([new Date((curtime-60*59)*1000-8*60*60*1000),new Date((curtime)*1000-8*60*60*1000)]);
		svg.selectAll("g").remove();
		
		drawentropy();
		
		var importantipg=svg.append("g").attr("class","importantip")
			.attr("transform", function(d, i) { return "translate("+(leftw+yaxisw)+"," + (upperheight+totallineheight+innerheight) + ")"; });
		drawipbytes(ipimportant,ipimportant_type,ipimportant_data,importantipg,0);
	
		var selectedipg=svg.append("g").attr("class","selectedip")
			.attr("transform", function(d, i) { return "translate("+(leftw+yaxisw)+"," + (upperheight+(totallineheight+innerheight)*(ipimportant.length+1)) + ")"; });
		drawipbytes(ipselected,ipselected_type,ipselected_data,selectedipg,1);
	
	}
	function drawentropy(){
		//求y轴domain
		var y_entropy = d3.scaleLinear().range([lineheight, 0]);
		var z_entropy = d3.scaleOrdinal(d3.schemeCategory10).domain([0,3]);
		var line_entropy = d3.line()
			.curve(d3.curveBasis)
			.x(function(d,i) { return x(new Date((curtime-60*59+i*60)*1000-8*60*60*1000)); })
			.y(function(d) { return y_entropy(d); });
		
		var tmpmin=entropydata[0][0];
		var tmpmax=entropydata[0][0];
		for(var i=0;i<entropydata.length;i++){
			var tmin=_.min(entropydata[i]);
			var tmax=_.max(entropydata[i]);
			if(tmin<tmpmin){tmpmin=tmin;}
			if(tmax>tmpmax){tmpmax=tmax;}
		}
		y_entropy.domain([tmpmin,tmpmax]);
		
		var entropyg=svg.append("g").attr("class","entropy")
			.attr("transform", function(d, i) { return "translate("+(leftw+yaxisw)+"," + (upperheight+textheight) + ")"; });
		var entropyline = entropyg.selectAll("g")
			.data(entropydata)
			.enter().append("g");
			
		entropyline.append("path")
			.attr("class", "line")
			.attr("d", function(d) { return line_entropy(d); })
			.style("stroke", function(d,i) { return entropycolor[i]; })
			.style("fill","none");
		entropyg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + (lineheight) + ")")
			.call(d3.axisBottom(x).ticks(5));
		entropyg.append("g")
			.attr("class", "y axis")
			.call(d3.axisLeft(y_entropy).ticks(5));
		entropyg.append("g").append("text")
			.attr("x", function(d,i){return 10;})
			.attr("y", 12.5-textheight)
			.text("entropy");
		var legend = entropyg.append("g").attr("class", "labeltext")
			.selectAll("g")
			.data(["srcip", "dstip", "dstport"])
			.enter().append("g")
			.attr("transform", function(d, i) { return "translate("+(80+60*i)+"," + (-textheight) + ")"; });
		legend.append("circle")
			.attr("cx", 0)
			.attr("cy", 10)
			.attr("r",5)
			.attr("fill",function(d,i){return entropycolor[i];})
		legend.append("text")
			.attr("x", function(d,i){return 10;})
			.attr("y", 12.5)
			.text(function(d,i) {;return d; });
	}
	
	function drawipbytes(iparr,iptype,ipdata,dom,adddel1){

		for(var k=0;k<ipdata.length;k++){
			var tmpdata=_.pluck(ipdata[k],"bytes");
			var y=d3.scaleLinear().range([lineheight, 0]).domain([_.min(tmpdata),_.max(tmpdata)]);
			//console.log([_.min(tmpdata),_.max(tmpdata)]);
			var ymax=_.max(tmpdata);
			var yformat=1e9;
			var yformatname=["G","M","K","B"];
			var yformatcnt=0;
			//while(ymax/yformat<1){yformat=yformat/1000;yformatcnt++;}
			for(var i=0;i<4;i++){yformat=yformat/1000;yformatcnt++;if(ymax/yformat>=1){break;}}
			
			var line=d3.line()
				.curve(d3.curveBasis)
				.x(function(d,i) { return x(new Date((curtime-60*59+i*60)*1000-8*60*60*1000)); })
				.y(function(d) { return y(d); });
			var ipline = dom.append("g")
				.attr("transform", function(d, i) { return "translate("+(0)+"," + ((totallineheight+innerheight)*k+textheight) + ")"; });
			ipline.append("g").append("path")
				.datum(tmpdata)
				.attr("class", "line")
				.attr("d", function(d,i) { return line(d); })
				.style("stroke", function(d,i) {
					if(iptype[k]=="src"){return srccolor;}
					else{return dstcolor;}
				})
				.style("fill","none");
			ipline.append("g")
				.attr("class", "x axis")
				.attr("transform", "translate(0," + (lineheight) + ")")
				.call(d3.axisBottom(x).ticks(5));
			ipline.append("g")
				.attr("class", "y axis")
				.call(d3.axisLeft(y).ticks(5, ",f").tickFormat(d3.formatPrefix(",.0", yformat)));
			
			var legend = ipline.append("g")
				.attr("transform", function(d, i) { return "translate("+(0)+"," + (-textheight-5) + ")"; });
			var legend_c=legend.append("circle")
				.attr("cx", 0)
				.attr("cy", 10)
				.attr("r",5)
				.attr("fill",function(d,i) {
					if(iptype[k]=="src"){return srccolor;}
					else{return dstcolor;}
				});
				
			legend.append("text")
				.attr("x", function(d,i){return 10;})
				.attr("y", 12.5)
				.text(function(){
					if(adddel1==1){return Observer.int2iP(iparr[k])+"___selected___"+iptype[k]}
					else{return Observer.int2iP(iparr[k])+"___main___"+iptype[k]}
				});
			legend_c.attr("id","ipbytes_"+adddel1+"_"+k)
				.on("dblclick",function(d,i){
					timer && clearTimeout(timer);
					//console.log(d3.event);
					//console.log($(this).attr("id"));
					var tmpipind=$(this).attr("id");
					if(parseInt(tmpipind.split("_")[1])==1){
						tmpipind=parseInt(tmpipind.split("_")[2]);
						ipselected.splice(tmpipind,1);
						ipselected_type.splice(tmpipind,1);
						ipselected_data.splice(tmpipind,1);
						hliparr=[];
						Observer.fireEvent("highlightip",[],line);
						drawgraph();
					}
					
				})
				.on("click",function(){
					var tmpid=$(this).attr("id");	
					var tmpthis=$(this);
					timer && clearTimeout(timer);
					timer=setTimeout(function(){//初始化一个延时
						//console.log(tmpid);
						tmpipind=parseInt(tmpid.split("_")[2]);
						var tmpip;
						if(parseInt(tmpid.split("_")[1])==1){
							tmpip=ipselected[tmpipind];
						}else{
							tmpip=ipimportant[tmpipind];
						}
						var tmpind=_.indexOf(hliparr,tmpip);
						if(tmpind>=0){
							hliparr=_.without(hliparr,tmpip);
							tmpthis.attr("class",null);
						}else{
							hliparr.push(tmpip);
							tmpthis.attr("class","hlip");
						}
						
						Observer.fireEvent("highlightip",hliparr,line);
					},250)
				});
		}
	}
	
	function selectip(){
		let obj = {};
		obj.endtime=JSON.stringify(curtime);
		obj.iparr=JSON.stringify(ipselected);
		obj.iptypearr=JSON.stringify(ipselected_type);
		$.ajax({
			type: 'GET',
			url: 'getipsbytes',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log("getipsbytes",ipselected);
				console.log(evt_data);
				ipselected_data=[];
				for(var i=0;i<ipselected.length;i++){
					ipselected_data.push(evt_data[ipselected[i]]);
				}
				drawgraph();
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	function changetime(){
		let obj = {};
		obj.endtime=JSON.stringify(curtime);
		$.ajax({
			type: 'GET',
			url: 'getimport',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log("get important ip");
				console.log(evt_data);
				ipimportant=[];
				ipimportant_data=[];
				if(evt_data["ip1"]!=-1){
					ipimportant.push(evt_data["ip1"]);
					ipimportant_type.push(evt_data["ip1type"]);
					ipimportant_data.push(evt_data["ip1data"]);
				}
				if(evt_data["ip2"]!=-1){
					ipimportant.push(evt_data["ip2"]);
					ipimportant_type.push(evt_data["ip2type"]);
					ipimportant_data.push(evt_data["ip2data"]);
				}
				$.ajax({
					type: 'GET',
					url: 'getentropy',
					data: obj,
					dataType: 'json',
					success: function(evt_data2) {
						console.log("get entropy");
						entropydata=[];
						var tmpkeys=_.keys(evt_data2);
						//console.log(tmpkeys);
						for (var i=0;i<tmpkeys.length;i++){
							var tmpdata=evt_data2[tmpkeys[i]];
							//console.log(tmpdata);
							//var tmpmax=_.max(tmpdata);
							//var tmpmin=_.min(tmpdata);
							//console.log(tmpmin,tmpmax);
							//entropydata[tmpkeys[i]]=_.map(entropydata[tmpkeys[i]], function(num){ return (num-tmpmin)/(tmpmax-tmpmin); });
							//evt_data2[tmpkeys[i]]=_.map(evt_data2[tmpkeys[i]], function(num){ return (num)/(tmpmax); });
							/*
							var mean = tmpdata.reduce(sum)/tmpdata.length;
							var deviations = tmpdata.map(function(x){return x-mean;});
							var stddev = Math.sqrt(deviations.map(square).reduce(sum)/(tmpdata.length-1));
							evt_data2[tmpkeys[i]]=_.map(evt_data2[tmpkeys[i]], function(num){ return (num-mean)/(stddev); });
							*/
							var mean = tmpdata.reduce(sum)/tmpdata.length;
							evt_data2[tmpkeys[i]]=_.map(evt_data2[tmpkeys[i]], function(num){ return (num-mean); });
						}
						console.log(evt_data2);
						entropydata.push(evt_data2["srcip"]);
						entropydata.push(evt_data2["dstip"]);
						//entropydata.push(evt_data2["srcport"]);
						entropydata.push(evt_data2["dstport"]);
						if(ipselected.length==0){
							drawgraph();
						}else{
							selectip();
						}
					},
					error: function(jqXHR) {
						console.log('post error!!', jqXHR);
					},
				});
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
				
    line.onMessage = function(message, data, from){
		//console.log(from); 
		if(message == "changeTimeRange" || message == "soinnend" || message == "changeTimeRange_skip"){
			//console.log(data);
			curtime=data[1]-60;
			$("#view1_wait").show(function(){
				var target= document.getElementById('view1_wait');
				spinner.spin(target);  
			});
			changetime();
		}
		if(message=="showipbytes"){
			//console.log(data);
			ipselected.push(data[0]);
			ipselected_type.push(data[1]);
			$("#view1_wait").show(function(){
				var target= document.getElementById('view1_wait');
				spinner.spin(target);  
			});
			selectip();
		}
		
	}
	
	
	Observer.addView(line);
	return line;
}
	
	
