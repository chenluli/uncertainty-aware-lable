
function Statistic(Observer){
	var statistic={};
	var $brtDiv=$("#view4");
    var width=$brtDiv.width();
    var height=$brtDiv.height();
	//console.log(width,height);
	
	var svg=d3.select("#view4")
			.append("svg")
			.attr("width", width)
			.attr("height", height);
			
	var svg_brush;
	var brush;
	
	var xaxisheight=60;
	var yaxiswidth=45;
	var margin = {top: 15, right: 20, bottom: 50, left: 20};
	var boxwidth = (width-yaxiswidth)/5 - margin.left - margin.right;
	var boxheight = height - margin.top - margin.bottom;

	statistic.curtype=0;//0:boxplot 1:scatter
	statistic.curiptype=0;//0:src 1:dest
	statistic.curxaxis=2;//0:occur cnt 1:bytes 2:dest port
	statistic.curyaxis=0;//0:occur cnt 1:bytes 2:dest port
	statistic.querytype=4;
	var typearr=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]];
	var keyarr=["cnt","bytes","port"];
	var groupnummax=6;
	
	function setquerytype(){
		//根据当前statistic属性决定要向后台查询的类型
		for(var i=0;i<typearr.length;i++){
			if(typearr[i][0]==statistic.curxaxis && typearr[i][1]==statistic.curyaxis){
				statistic.querytype=i;
				break;
			}
		}
	}
	
	$("#st_reset").click(function(){
		statistic.curtype=parseInt(document.getElementById("st_type").value);
		statistic.curiptype=parseInt(document.getElementById("st_ip").value);
		statistic.curxaxis=parseInt(document.getElementById("st_xaxis").value);
		statistic.curyaxis=parseInt(document.getElementById("st_yaxis").value);
		clearbrush();
		setquerytype();
		resetgraph(curTime,curTime+60);
	})
	
	var curTime=Observer.starttime;//1365078600;1365062520
	
	var abnormalscale=3;
	
	//boxplot中选中的点
	/*
	var circle0rect1=-1;
	var circleclicked=-1;
	var rectclickedmin=-1;
	var rectclickedmax=-1;
	*/
	var boxseliparr=[];
	//var boxhliparr=[];
	
	var boxmin = Infinity;var boxmax = -Infinity;
	var spliteddataobj=[];
	var spliteddataarr=[];
	var boxrange=[];
	
	var boxxloc=[];
	var boxyscale;
	
	var boxchart = d3.box()
		.whiskers(iqr(abnormalscale))
		.width(boxwidth)
		.height(boxheight);
		
	//scatter
	var scatterdata=[];
	var scatterseliparr=[];
	var scatterxscale;
	var scatteryscale;
	var scattercircles;
	
	//var scatterhliparr=[];
	var highlightiparr=[];
	//var highlightiparr=[2886992330,2886992332,170319288,169556837];
	
	function resetgraph(starttime,endtime){
		//console.log(width,height);
		let obj = {};
		obj.starttime=JSON.stringify(starttime);
		obj.endtime=JSON.stringify(endtime);
		obj.querytype=JSON.stringify(statistic.querytype);
		obj.iptype=JSON.stringify(statistic.curiptype);
		console.log(obj);

		$.ajax({
			type: 'GET',
			url: 'statisticdata',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				//如果y轴是bytes，取对数
				if(keyarr[statistic.curyaxis]=="bytes"){
					for(var i=0;i<evt_data.data.length;i++){
						evt_data.data[i]["bytes"]=Math.log(evt_data.data[i]["bytes"]+1);
					}
				}
				//如果x轴或y轴是port，合并大于2014的数据
				if(keyarr[statistic.curxaxis]=="port" || keyarr[statistic.curyaxis]=="port"){
					for(var i=0;i<evt_data.data.length;i++){
						if(parseInt(evt_data.data[i]["port"])>1024){
							//console.log(evt_data.data[i]);
							evt_data.data[i]["port"]=1025;
						}
					}
				}
				
				if(statistic.curtype==0){
					//draw boxplot
					drawboxplot(evt_data.data);
					boxhightlight();
				}else{
					drawscatter(evt_data.data);
					scatterhightlight();
				}
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
		
	}
	resetgraph(curTime,curTime+60);
	
	function drawboxplot(data){
		//console.log(data);
		boxseliparr=[];
		
		//获取总体数据的y轴属性的最大最小值
		var ydata=_.pluck(data,keyarr[statistic.curyaxis]);
		boxmax=_.max(ydata);
		boxmin=_.min(ydata);
		//console.log(boxmin,boxmax);
		//把data按照x轴类型分割
		spliteddataobj=[];
		if(keyarr[statistic.curxaxis]=="port" || data.length<=groupnummax){
			//如果x轴是端口，可能的取值比较少，不用聚合
			for(var i=0;i<data.length;i++){
				if(spliteddataobj.length==0 ||
					spliteddataobj[spliteddataobj.length-1][0][keyarr[statistic.curxaxis]] != data[i][keyarr[statistic.curxaxis]]){
						spliteddataobj.push([]);
						spliteddataobj[spliteddataobj.length-1].push(data[i]);
				}else{
					spliteddataobj[spliteddataobj.length-1].push(data[i]);
				}
			}
		}else{
			//否则根据x轴取值聚合成groupnummax组
			var splitnum=[];
			for (var i=0;i<groupnummax;i++){
				splitnum.push(parseInt(data.length/(groupnummax)*i));
			}
			splitnum.push(data.length);
			for(var i=0;i<splitnum.length-1;i++){
				spliteddataobj.push(data.slice(splitnum[i],splitnum[i+1]));
			}
		}
		spliteddataobj.push(data);
		console.log(spliteddataobj);
		//分割后提取obj中的y轴属性并排序
		spliteddataarr=[];
		for(var i=0;i<spliteddataobj.length;i++){
			spliteddataarr.push(_.pluck(spliteddataobj[i],keyarr[statistic.curyaxis]));
		}
		for(var i=0;i<spliteddataarr.length;i++){
		    spliteddataarr[i].sort(function(a,b){return a-b;});
	    }
		console.log(spliteddataarr);
		
		//设置boxplot的domain，开始绘制
		boxwidth= (width-yaxiswidth)/(spliteddataarr.length) - margin.left - margin.right;
		//console.log(width,spliteddataarr.length,boxwidth);
		boxrange=[];
		boxchart.width(boxwidth)
				.domain([boxmin, boxmax]);

		svg.selectAll("g").remove();
		var svg_g=svg.selectAll("g")
			.data(spliteddataarr)
			.enter().append("g")
			.attr("class", function(d,i){return "box box"+i;})
			.attr("transform", function(d,i){return "translate(" + (yaxiswidth+i*((width-yaxiswidth)/(spliteddataarr.length))+margin.left) + "," + margin.top + ")";})
			.call(boxchart);

		var xscale,xAxis,yAxis;
		[boxxloc,xscale,xAxis,boxyscale,yAxis]=setaxis(data,1,spliteddataobj);
		
		svg.append("g")
			.attr("class", "x axis xordinal")
			.attr("transform", "translate("+(margin.left)+"," + (height - xaxisheight+20) + ")")
			.call(xAxis);
			
		svg.append("g")
			.attr("class", "y axis")
			.attr("transform", "translate("+(yaxiswidth-8)+"," + (margin.top)+ ")")
			.call(yAxis);
			
		//brush
		brush = d3.brush()
			.extent([[0, 0], [width-yaxiswidth-margin.right-margin.left+6, boxheight+6]])
			.on("end", brushended);
			
		function brushended() {

			if (!d3.event.sourceEvent) return; // Only transition after input.
			if (!d3.event.selection){return;} // Ignore empty selections.
			//console.log(d3.event.selection);
			if(highlightiparr.length!=0){
				highlightiparr=[];
				boxhightlight();
			}
			
			var s=(d3.event.selection);
			var xmax,xmin,ymax,ymin;
			xmax = Math.max(s[0][0],s[1][0]);
			xmin = Math.min(s[0][0],s[1][0]);
			ymax = Math.max(s[0][1],s[1][1]);
			ymin = Math.min(s[0][1],s[1][1]);
			//console.log("x: ",xmin,xmax);
			//console.log("y: ",ymin,ymax);
			var tmpxind=_.sortedIndex(boxxloc, xmin);
			//console.log(tmpxind);
			var tmpipinrange=[];
			for(var i=0;i<spliteddataobj[tmpxind].length;i++){
				var tmpy=boxyscale(spliteddataobj[tmpxind][i][keyarr[statistic.curyaxis]]);
				if(tmpy>=ymin && tmpy<=ymax){
					tmpipinrange.push(spliteddataobj[tmpxind][i]["ip"]);
				}
			}
			boxseliparr=tmpipinrange;
			console.log(boxseliparr);
			Observer.fireEvent("highlightip",boxseliparr,statistic);
			//svg_brush.call(brush.move, null);
		}
		svg_brush=svg.append("g")
			.attr("class", "brush")
			.attr("transform", function(d,i){return "translate(" + (yaxiswidth+i*((width-yaxiswidth)/(spliteddataarr.length))+margin.left-3) + "," + (margin.top-3) + ")";})
			.call(brush);
		svg_brush.on("dblclick",function(d){
			Observer.fireEvent("highlightip",[],statistic);
		});
	}
	
	function clearbrush(){
		svg_brush.call(brush.move, null);
		boxseliparr=[];
		scatterseliparr=[];
	}
	//soinn.boxhightlight=function(){
	function boxhightlight(){
		var tmpdata_circle=[];
		var tmpdata_line=[];
		for(var i=0;i<spliteddataobj.length;i++){
			for(var j=0;j<spliteddataobj[i].length;j++){
				if(_.indexOf(highlightiparr,spliteddataobj[i][j]["ip"])>=0){
					var tmpydata=spliteddataobj[i][j][keyarr[statistic.curyaxis]];
					if(tmpydata>=boxrange[i][0] && tmpydata<=boxrange[i][1]){
						tmpdata_line.push({"boxid":i,"data":tmpydata});
					}else{
						tmpdata_circle.push({"boxid":i,"data":tmpydata});
					}
				}
			}
		}
		//console.log(tmpdata_circle);
		//console.log(tmpdata_line);
		svg.selectAll(".boxhlip").remove();
		var svgboxhl=svg.append("g").attr("class","boxhlip")
			.attr("transform", function(d,i){return "translate(" + (margin.left) + "," + margin.top + ")";});
			
		svgboxhl.selectAll("circle")
			.data(tmpdata_circle).enter()
			.append("circle").attr("class","hl")
			.attr("cx",function(d){return boxxloc[d.boxid];})
			.attr("cy",function(d){return boxyscale(d.data);})
			.attr("r",6);
		svgboxhl.selectAll("line")
			.data(tmpdata_line).enter()
			.append("line").attr("class","hl")
			.attr("x1",function(d){return boxxloc[d.boxid]-boxwidth/2;})
			.attr("x2",function(d){return boxxloc[d.boxid]+boxwidth/2;})
			.attr("y1",function(d){return boxyscale(d.data);})
			.attr("y2",function(d){return boxyscale(d.data);});
	}
	// Returns a function to compute the interquartile range.
	function iqr(k) {
		return function(d, i) {
			//console.log(d);
			var q1 = d.quartiles[0],
				q3 = d.quartiles[2],
				iqr = (q3 - q1) * k,
				i = -1,
				j = d.length;
			while (d[++i] < q1 - iqr);
			while (d[--j] > q3 + iqr);
			//console.log([q1 - iqr,q3 + iqr]);
			//console.log([i, j]);
			boxrange.push([q1 - iqr,q3 + iqr]);
			return [i, j];
		};
	}
	
	function setaxis(data,group1other0,spliteddataobj){
		//width=$brtDiv.width();
		//height=$brtDiv.height();
		//console.log(height);
		var xdata=_.pluck(data,keyarr[statistic.curxaxis]);
		var ydata=_.pluck(data,keyarr[statistic.curyaxis]);
		//x轴
		var xAxis;
		var xtext=[];
		var xscale;
		var xAxis;
		var xloc=[];
		if(keyarr[statistic.curxaxis]=="port" || data.length<=groupnummax || group1other0==1){
			if(keyarr[statistic.curxaxis]=="port" || data.length<=groupnummax){
				xtext=_.pluck(data,keyarr[statistic.curxaxis]);
				xtext=_.uniq(xtext,true);
				if(statistic.curtype==0){xtext.push("all");}
			}else{
				for(var i=0;i<spliteddataobj.length;i++){
					var start=spliteddataobj[i][0][keyarr[statistic.curxaxis]];
					var end=spliteddataobj[i][spliteddataobj[i].length-1][keyarr[statistic.curxaxis]];
					xtext.push((i+1)+":"+start+"-"+end);
				}
				xtext.push("all");
			}
			if(statistic.curtype==0){
				xloc=_.map(_.range(xtext.length), function(num){ 
					return (width-yaxiswidth)/xtext.length*(num)+boxwidth/2+yaxiswidth; 
				});
			}else{
				xloc=_.map(_.range(xtext.length), function(num){ 
					return (width-yaxiswidth-margin.right)/xtext.length*(num+0.5)+yaxiswidth; 
				});
			}
			
			xscale = d3.scaleOrdinal()
				.domain(xtext)
				.range(xloc);
			xAxis = d3.axisBottom().scale(xscale).tickValues(xtext);
		}else{
			xscale = d3.scaleLinear()
				.domain([_.min(xdata),_.max(xdata)])
				.range([0,width-yaxiswidth-margin.right]);
			xAxis = d3.axisBottom().scale(xscale).ticks(5, ",f");
			if(keyarr[statistic.curxaxis]=="bytes"){
				var xformat=1e9;
				var maxd=_.max(xdata);
				while(maxd/xformat<10){xformat=xformat/1000;}
				xAxis.tickFormat(d3.formatPrefix(",.0", xformat));
			}
		}
		
		//y轴
		var yAxis;
		var ytext=[];
		var yscale;
		var yAxis;
		var yloc=[];
		if(keyarr[statistic.curyaxis]=="port" && statistic.curtype==1){
			ytext=_.pluck(data,keyarr[statistic.curyaxis]);
			ytext=_.uniq(ytext);
			ytext.sort(function(a,b){return b-a;});
			var yloc=_.map(_.range(ytext.length), function(num){ 
				return (height-xaxisheight-margin.top)/(ytext.length-1)*(num);//+margin.top; 
			});
			//console.log(ytext,yloc)
			yscale = d3.scaleOrdinal()
				.domain(ytext)
				.range(yloc);
			yAxis = d3.axisLeft().scale(yscale).tickValues(ytext);
		}else{
			if(statistic.curtype==0){var rang=[boxheight, 0];}
			else{var rang=[height-xaxisheight-margin.top, 0];}
			yscale = d3.scaleLinear()
				.range(rang)
				.domain([_.min(ydata),_.max(ydata)]);
			yAxis = d3.axisLeft().scale(yscale).ticks(5, ",f");
		}
		if(keyarr[statistic.curyaxis]=="bytes"){
			var yformat=1e9;
			while(boxmax/yformat<1){yformat=yformat/1000;}
			yAxis.tickFormat(d3.formatPrefix(",.0", yformat));
		}
		return [xloc,xscale,xAxis,yscale,yAxis];
	}
	
	function drawscatter(data){
		svg.selectAll("g").remove();
		scatterdata=data;
		scatterseliparr=[];

		var xloc,xAxis,yAxis;
		[xloc,scatterxscale,xAxis,scatteryscale,yAxis]=setaxis(data,0,[]);
		console.log(scatteryscale.range());
		svg.append("g")
			.attr("class", function(){
				if(keyarr[statistic.curxaxis]=="port"){return "x axis xordinal";}
				else{return "x axis";}
			})
			.attr("transform", "translate("+(yaxiswidth)+"," + (height - xaxisheight) + ")")
			.call(xAxis);
		svg.append("g")
			//.attr("class", "y axis")
			.attr("class", function(){
				if(keyarr[statistic.curyaxis]=="port"){return "y axis xordinal";}
				else{return "y axis";}
			})
			.attr("transform", "translate("+(yaxiswidth)+"," + (margin.top)+ ")")
			.call(yAxis);
			
		//scatter
		scattercircles=svg.append("g")
			.attr("transform", function(d,i){return "translate(" + (yaxiswidth) + "," + margin.top + ")";})
			.selectAll("circle")
			.data(data)
			.enter().append("circle")
			.attr("class", "scatter_circle")
			.attr("cx",function(d){return scatterxscale(d[keyarr[statistic.curxaxis]]);})
			.attr("cy",function(d){return scatteryscale(d[keyarr[statistic.curyaxis]]);})
			.attr("r",5);
		//brush
		brush = d3.brush()
			.extent([[0, 0], [width-yaxiswidth-margin.right+6, height-xaxisheight-margin.top+6]])
			.on("end", brushended);
			
		function brushended() {
			if (!d3.event.sourceEvent) {return;} // Only transition after input.
			if (!d3.event.selection) {return;} // Ignore empty selections.
			if(highlightiparr.length!=0){
				highlightiparr=[];
				scatterhightlight();
			}
			var s=(d3.event.selection);
			var xmax,xmin,ymax,ymin;
			xmax = Math.max(s[0][0],s[1][0]);xmin = Math.min(s[0][0],s[1][0]);
			ymax = Math.max(s[0][1],s[1][1]);ymin = Math.min(s[0][1],s[1][1]);

			var tmpipinrange=[];
			for(var i=0;i<scatterdata.length;i++){
				var tmpx=scatterxscale(scatterdata[i][keyarr[statistic.curxaxis]]);
				var tmpy=scatteryscale(scatterdata[i][keyarr[statistic.curyaxis]]);
				if(tmpy>=ymin && tmpy<=ymax && tmpx>=xmin && tmpx<=xmax){
					tmpipinrange.push(scatterdata[i]["ip"]);
				}
			}
			scatterseliparr=tmpipinrange;
			console.log(scatterseliparr);
			Observer.fireEvent("highlightip",scatterseliparr,statistic);
		}
		svg_brush=svg.append("g")
			.attr("class", "brush")
			.attr("transform", function(d,i){return "translate(" + (yaxiswidth-3) + "," + (margin.top-3) + ")";})
			.call(brush);
		svg_brush.on("dblclick",function(d){
			Observer.fireEvent("highlightip",[],statistic);
		});	
	}
	function scatterhightlight(){
	//soinn.scatterhightlight=function(){
		var tmpdata_circle = _.filter(scatterdata, function(d){ 
			return _.indexOf(highlightiparr,d["ip"]) >= 0; 
		});
		//console.log(tmpdata_circle);
		svg.selectAll(".scatterhlip").remove();
		var svgscatterhl=svg.append("g").attr("class","scatterhlip")
			.attr("transform", function(d,i){return "translate(" + (yaxiswidth) + "," + margin.top + ")";});
			
		svgscatterhl.selectAll("circle")
			.data(tmpdata_circle).enter()
			.append("circle").attr("class","hl")
			.attr("cx",function(d){return scatterxscale(d[keyarr[statistic.curxaxis]]);})
			.attr("cy",function(d){return scatteryscale(d[keyarr[statistic.curyaxis]]);})
			.attr("r",6);
	}
	
    statistic.onMessage = function(message, data, from){
		
		if(message == "changeTimeRange" || message == "updateMinute" || message == "changeTimeRange_skip"){
			//console.log(data);
			curTime=data[0];
			resetgraph(data[0],data[1]);
		}
		if(message=="highlightip" && from!=statistic){
			//console.log(data); 
			highlightiparr=data;
			
			clearbrush();
			if(statistic.curtype==0){
				boxhightlight();
			}else{
				scatterhightlight();
			}
		}
		
		
	}
	
	
	Observer.addView(statistic);
	return statistic;
}
	
	
