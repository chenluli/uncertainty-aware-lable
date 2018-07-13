function Timeline(Observer) {
    var timeline = {};
	
	var $btDiv=$("#timeline-view");
    var width=$btDiv.width()-5;
    var height=$btDiv.height()-5;
	//console.log(width,height);
	
	var svg=d3.select("#timeline-view")
			.append("svg")
			.attr("width", width)
			.attr("height", height);
	
	timeline.Interval_time=10000;//ms
	//timeline.Interval;
	
	timeline.startTime=1364774400;//开始时间
	timeline.curTime=Observer.starttime;//实时进行到的时间，不断+60s，递增
	//timeline.curTime_bak=Observer.starttime;//实时进行到的时间，不断+60s，递增
	
	timeline.daynum=7;
	timeline.hournum=24;
	timeline.minutenum=60;
	
	var intermargin=35;//三个timeline之间的间隔
	var labelwidth=90;//三个timeline左侧label的宽度
	var aboveblankheight=22;//timeline上方留白的高度
	var bottomblankheight=25;//timeline下方留白的高度（包括坐标轴）
	
	var time_day_width=(width-4*intermargin-labelwidth)*timeline.daynum/(timeline.daynum+timeline.hournum+timeline.minutenum);//日 timeline的宽度
	var time_hour_width=(width-4*intermargin-labelwidth)*timeline.hournum/(timeline.daynum+timeline.hournum+timeline.minutenum);//小时 timeline的宽度
	var time_minute_width=(width-4*intermargin-labelwidth)*timeline.minutenum/(timeline.daynum+timeline.hournum+timeline.minutenum);//分钟 timeline的宽度
	
	timeline.protocol_stack_keys=["tcp","udp","others"];
	timeline.protocol_stack_colors=["#AFC0DD","#90ABDD","#465674"];
	timeline.protocol_selected_colors=["#F6E3BE","#F6D598","#AE9361"];
	timeline.port_stack_keys=["http","ftp","mail","NetBIOS","reflect","others"];
	timeline.port_stack_colors=["#AFC0DD","#90ABDD","#465674","#486598","#273A5E","#32486C"];
	timeline.port_selected_colors=["#F6E3BE","#F6D598","#AE9361","#E5B660","#8E6D31","#986E21"];

	var curtype1=0;var curtype2=0;
	var typecorr={"all":0,"src":1,"dst":2,"protocol":0,"port":3};
	timeline.currentType=0;
	var typelabelvar=[timeline.protocol_stack_keys, timeline.protocol_stack_keys, timeline.protocol_stack_keys
					 ,timeline.port_stack_keys, timeline.port_stack_keys, timeline.port_stack_keys];
	var typecolorvar=[timeline.protocol_stack_colors, timeline.protocol_stack_colors, timeline.protocol_stack_colors
					 ,timeline.port_stack_colors, timeline.port_stack_colors, timeline.port_stack_colors];
	var typecolor_selected_var=[timeline.protocol_selected_colors, timeline.protocol_selected_colors, timeline.protocol_selected_colors
					 ,timeline.port_selected_colors, timeline.port_selected_colors, timeline.port_selected_colors];
	
	timeline.selectedKey=typelabelvar[timeline.currentType];
	timeline.selectedKey_color=typecolorvar[timeline.currentType];
	timeline.selectedKey_color_sel=typecolor_selected_var[timeline.currentType];
	
	/*
	0:TotalBytes all protocol
	1:TotalBytes src protocol
	2:TotalBytes dst protocol
	3:TotalBytes all port
	4:TotalBytes src port
	5:TotalBytes dst port
	*/
	
	
	//index from 0
	timeline.dayselected=[3];//当前选中的day
	timeline.hourselected=[12];//当前选中的hour
	timeline.minuteselected=[30];//当前选中的minute
	var mindownstarttmp=-1;//选中的minute的开始
	var minupendtmp=-1;//选中的minute的结束
	
	var selectedSOINN=-1;
	var selectedSOINN_tlind=-1;
	var daytimeind_hl=-1;var hourtimeind_hl=-1;var minutetimeind_hl=-1;//高亮的stack的index
	

	//var timedata;
	
	var x_day;var x_day_full;var y_day;var z_day;var z_day_selected;
	var xAxis_day;var xAxis_day_full;var yAxis_day;
	var tipday;
	var day_timeline=svg.append("g").attr("transform", "translate(" + (labelwidth) + "," + 0 + ")");
	var day_stack;var day_stack_g;
	
	var x_hour;var x_hour_full;var y_hour;var z_hour;var z_hour_selected;
	var xAxis_hour;var xAxis_hour_full;var yAxis_hour;
	var tiphour;
	var hour_timeline=svg.append("g").attr("transform", "translate(" + (labelwidth+intermargin+time_day_width) + "," + 0 + ")");
	var hour_stack;var hour_stack_g;
	
	var x_minute;var x_minute_full;var y_minute;var z_minute;var z_minute_selected;
	var xAxis_minute;var xAxis_minute_full;var yAxis_minute;
	var tipminute;
	var minute_timeline=svg.append("g").attr("transform", "translate(" + (labelwidth+2*intermargin+time_day_width+time_hour_width) + "," + 0 + ")");
	var minute_stack;var minute_stack_g;
	
	function init_scale_axis(data,timeline_width,barnum,p_keys,p_colors,selectedcolor,timeline_dom,xaxisstr){
		//初始化比例尺和坐标轴
		//x轴要显示的整体范围
		var timeaxistext=[];
		for(var i=0;i<barnum;i++){
			var j=i+1;
			if(j<10){timeaxistext.push("0"+j);}
			else{timeaxistext.push(""+j);}
		}
		var odds_timeaxistext = _.reject(timeaxistext, function(num){ return num % 2 == 0; });
		
		//定义比例尺
		var x = d3.scaleBand().rangeRound([0, timeline_width]).paddingInner(0.1);
		var x_full = d3.scaleBand().rangeRound([0, timeline_width]).paddingInner(0.1);
		var y = d3.scaleLinear().range([height-bottomblankheight, aboveblankheight]);
		var z = d3.scaleOrdinal().range(p_colors);
		var z_selected = d3.scaleOrdinal().range(selectedcolor);
		
		//比例尺输入范围
		xdom=_.pluck(data,"tm");
		while(xdom.length<barnum){xdom.push(xdom[xdom.length-1]+60);}
		x.domain(xdom);
		//console.log(x.domain())
		x_full.domain(timeaxistext);
		var ymax=d3.max(data,function (d) {var t=0; for(var k=0;k<p_keys.length;k++){t=t+d[p_keys[k]];};return t; })
		y.domain([0, ymax]).nice();
		z.domain(p_keys);
		z_selected.domain(p_keys);
		
		//y轴显示的format
		var yformat=1e9;
		var yformatname=["G","M","K","B"];
		var yformatcnt=0;
		while(ymax/yformat<1){yformat=yformat/1000;yformatcnt++;}
		
		//tip
		var tiptool = d3.tip()
				.attr('class', 'd3-tip timelinetip')
				.html(function(d,i){return daytip(d);})
				.offset([-10, 0]);
		svg.call(tiptool);
		
		function daytip(d){
			var t=0; 
			for(var k=0;k<p_keys.length;k++){t=t+d.data.data[p_keys[k]]};
			t=t/yformat;t=t.toFixed(2);
			return "<strong>"+d.type+" </strong>"+
				"<strong>Total:</strong> <span style='color:red'>" + t+yformatname[yformatcnt]+"</span>"+
				"&nbsp;&nbsp;<strong>Volume:</strong> <span style='color:red'>" + ((d.data[1]-d.data[0])/yformat).toFixed(2) +yformatname[yformatcnt]+ "</span>";
		}
		//定义坐标轴
		var xAxis = d3.axisBottom().scale(x_full).tickValues(odds_timeaxistext);
		var yAxis = d3.axisLeft().scale(y).ticks(5, ",f").tickFormat(d3.formatPrefix(",.0", yformat));
		//插入坐标轴
		timeline_dom.selectAll(".axis").remove();
		timeline_dom.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate("+(intermargin)+"," + (height-bottomblankheight+3) + ")")
			.call(xAxis)
			.append("text")
			.attr("x", x_full.range()[1]+10)
			.attr("dy", "1.5em")
			.text(xaxisstr);

		timeline_dom.append("g")
			.attr("class", "y axis")
			.attr("transform", "translate("+(intermargin-3)+"," + 0+ ")")
			.call(yAxis)
			.append("text")
			.attr("x", intermargin*0.2).attr("y", aboveblankheight-22)
			.attr("dy", "1.4em")
			.style("text-anchor", "end")
			.text("Bytes");
		
		return [x,x_full,y,z,z_selected,xAxis,yAxis,tiptool];
	}
	
	function init_stacks(data,p_keys,selectedarr,x,y,z,z_selected,tiptool,timeline_dom,xaxisstr,hlarr){
		//初始化堆叠直方图
		timeline_dom.selectAll("."+xaxisstr).remove();
		var barstack_g=timeline_dom.append("g").attr("class",xaxisstr)
			.attr("transform", "translate(" + intermargin + "," + 0 + ")")
			.selectAll("g")
			.data(d3.stack().keys(p_keys)(data))
			.enter().append("g").attr("class",function(d,i){return d.key;})
			.attr("fill", function(d,i){return z(d.key);});
		var barstack=barstack_g.selectAll("rect")
			.data(function(d) { return d; })
			.enter().append("rect")
			.attr("fill", function(d,i){
				if (_.indexOf(selectedarr,i)>=0){return z_selected($(this).parent().attr("class"));}
			})
			.attr("opacity",function(d,i){
				if(hlarr==-1 || _.indexOf(hlarr,i,true)>=0){return 1;}
				else{return 0.3;}
			})
			.attr("x", function(d) { return x(d["data"]["tm"]); })
			.attr("y", function(d) { return y(d[1]); })
			.attr("height", function(d) { return y(d[0]) - y(d[1]); })
			.attr("width", x.bandwidth())
			//.on('mouseover', tiptool.show)
			.on('mouseover', function(d,i){tiptool.show({"data":d,"type":$(this).parent().attr("class")},i);})
			.on('mouseout', tiptool.hide);
		return [barstack_g,barstack];
	}
	
	function init_all_scale(stack_keys,stack_colors,selected_colors){
		d3.selectAll(".timelinetip").remove();
		[x_day,x_day_full,y_day,z_day,z_day_selected,xAxis_day,yAxis_day,tipday]=
			init_scale_axis(timeline.timedata["day"], time_day_width, timeline.daynum, stack_keys,
			stack_colors, selected_colors, day_timeline, "Day");
		[x_hour,x_hour_full,y_hour,z_hour,z_hour_selected,xAxis_hour,yAxis_hour,tiphour]=
			init_scale_axis(timeline.timedata["hour"], time_hour_width, timeline.hournum, stack_keys,
			stack_colors, selected_colors, hour_timeline, "Hour");
		[x_minute,x_minute_full,y_minute,z_minute,z_minute_selected,xAxis_minute,yAxis_minute,tipminute]=
			init_scale_axis(timeline.timedata["minute"], time_minute_width, timeline.minutenum, stack_keys,
			stack_colors, selected_colors, minute_timeline, "Minute");
	}
	function init_all_stacks(stack_keys){
		[day_stack_g,day_stack]=
			init_stacks(timeline.timedata["day"],stack_keys,timeline.dayselected,
			x_day,y_day,z_day,z_day_selected,tipday,day_timeline,"day",daytimeind_hl);
		[hour_stack_g,hour_stack]=
			init_stacks(timeline.timedata["hour"],stack_keys,timeline.hourselected,
			x_hour,y_hour,z_hour,z_hour_selected,tiphour,hour_timeline,"hour",hourtimeind_hl);
		[minute_stack_g,minute_stack]=
			init_stacks(timeline.timedata["minute"],stack_keys,timeline.minuteselected,
			x_minute,y_minute,z_minute,z_minute_selected,tipminute,minute_timeline,"minute",minutetimeind_hl);
	}
	function inittimeline(stack_keys,stack_colors,selected_colors){
		//console.log(stack_keys,stack_colors,selected_colors)
		init_all_scale(stack_keys,stack_colors,selected_colors);
		init_all_stacks(stack_keys);
		bindclick();
		svg.selectAll("rect").attr("rx","1.5px");
	}
	
	function bindclick(){
		//绑定堆叠图点击事件
		day_stack.on("click",function(d,i){
				if (timeline.dayselected[0]!=i){
					timeline.dayselected[0]=i;
					day_stack.attr("fill", function(dd,ii){
						if (ii==i){return z_day_selected($(this).parent().attr("class"));}
						else {return z_day($(this).parent().attr("class"));}
					})
					var clikedstack=$(this).parent().parent().attr("class");
					var tmptime=timeline.timedata[clikedstack][i]["tm"];
					var daydiffer=Math.floor((timeline.curTime-tmptime)/(24*3600))
					if(daydiffer>=1){//选了之前的天
						timeline.hourselected=[23];
						timeline.minuteselected=[59];
					}else{//选回了最近的天
						var tmpDate=new Date(timeline.curTime*1000-8*60*60*1000);
						timeline.hourselected=[tmpDate.getHours()];
						timeline.minuteselected=[tmpDate.getMinutes()];
					}
					changeDay();
				}
			});
		hour_stack.on("click",function(d,i){
				if (timeline.hourselected[0]!=i){
					timeline.hourselected[0]=i;
					hour_stack.attr("fill", function(dd,ii){
						if (ii==i){return z_hour_selected($(this).parent().attr("class"));}
						else {return z_hour($(this).parent().attr("class"));}
					})
					//选hour，day不变
					var clikedstack=$(this).parent().parent().attr("class");
					var tmptime=timeline.timedata[clikedstack][i]["tm"];
					var hourdiffer=(timeline.curTime-tmptime)%(24*3600); 
					var hourdiffer=Math.floor(hourdiffer/(3600));
					//console.log(hourdiffer);
					if(hourdiffer>=1){
						timeline.minuteselected=[59];
					}else{
						var tmpDate=new Date(timeline.curTime*1000-8*60*60*1000);
						timeline.minuteselected=[tmpDate.getMinutes()];
					}
					changeDay();
				}
			});
		function minute_select_event(d,i){
			//移动过程中，更新timeline.minuteselected
			//对minute的bar重新填充颜色
			minupendtmp=i;
			timeline.minuteselected=[];
			for(var k=_.min([mindownstarttmp,minupendtmp]);k<=_.max([mindownstarttmp,minupendtmp]);k++){
				timeline.minuteselected.push(k);
			}
			minute_stack.attr("fill", function(dd,ii){
				if (ii>=timeline.minuteselected[0] && 
						ii<=timeline.minuteselected[timeline.minuteselected.length-1]){
					return z_minute_selected($(this).parent().attr("class"));
				}
				else {return z_minute($(this).parent().attr("class"));}
			})
		}
		minute_stack.on("mousedown",function(d,i){mindownstarttmp=i;})
			.on("mouseenter",function(d,i){
				//console.log("lll");
				if(mindownstarttmp==-1){return;}
				minute_select_event(d,i)
			})
			.on("mouseup",function(d,i){
				minute_select_event(d,i)
				mindownstarttmp=-1;minupendtmp=-1;
				console.log(timeline.minuteselected);
				resetHighlight();
				var tmpsttime=timeline.timedata["minute"][timeline.minuteselected[0]]["tm"];
				var tmpendtime=timeline.timedata["minute"][timeline.minuteselected[timeline.minuteselected.length-1]]["tm"]+60;
				console.log("timerange",tmpsttime,tmpendtime);
				Observer.fireEvent("changeTimeRange",[tmpsttime,tmpendtime],timeline);
			});
	}
	
	function init_legend(){
		//图例
		//初始化
		svg.selectAll(".labeltext").remove();
		//timeline.selectedKey=typelabelvar[timeline.currentType]
		
		var legend = svg.append("g")
			.attr("class", "labeltext")
			.selectAll("g")
			.data(typelabelvar[timeline.currentType].slice())
			.enter().append("g")
			.attr("transform", function(d, i) { return "translate("+10+"," + (12+17*i) + ")"; });

		legend.append("rect")
			.attr("x", 0)
			.attr("y", 0)
			.attr("width", 9)
			.attr("height", 9)
			.attr("fill", function(d,i){
				if(_.indexOf(timeline.selectedKey,d)>=0){return z_day(d);}
				else{return "#222";}
			})
			.attr("stroke","white")
			.attr("stroke-width",1)
			.on("click",function(d,i){
				var tmpflag=0;
				if(_.indexOf(timeline.selectedKey,d)>=0){
					tmpflag=1;timeline.selectedKey=_.without(timeline.selectedKey,d);
				}else{
					timeline.selectedKey.push(d);
				}
				
				var tmpcolor=[];
				var tmpcolor_selected=[];
				for(var ii=0;ii<timeline.selectedKey.length;ii++){
					var tmpind=_.indexOf(typelabelvar[timeline.currentType],timeline.selectedKey[ii])
					if(tmpind>=0){
						tmpcolor.push(typecolorvar[timeline.currentType][tmpind]);
						tmpcolor_selected.push(typecolor_selected_var[timeline.currentType][tmpind]);
					}
				}
				timeline.selectedKey_color=tmpcolor;
				timeline.selectedKey_color_sel=tmpcolor_selected;
				inittimeline(timeline.selectedKey,timeline.selectedKey_color,timeline.selectedKey_color_sel);
				if(tmpflag==1){$(this).attr("fill","#222");}else{$(this).attr("fill",z_day(d));}
			});
		
		legend.append("text")
			.attr("x", 12)
			.attr("y", 8)
			.text(function(d) {;return d; });
	}
	
	function changeType(){
		$("input[name='online-checkbox']").bootstrapSwitch('state', false);
		let obj = {};
		obj.type = JSON.stringify(timeline.currentType);
		$.ajax({
			type: 'GET',
			url: 'changeType',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				timeline.timedata=evt_data;
				timeline.selectedKey=typelabelvar[timeline.currentType];
				timeline.selectedKey_color=typecolorvar[timeline.currentType];
				timeline.selectedKey_color_sel=typecolor_selected_var[timeline.currentType];
				//inittimeline(typelabelvar[timeline.currentType],typecolorvar[timeline.currentType],typecolor_selected_var[timeline.currentType])
				calcuTimeOpacity(selectedSOINN_tlind);
				inittimeline(timeline.selectedKey,timeline.selectedKey_color,timeline.selectedKey_color_sel)
				init_legend();
				svg.selectAll("rect").attr("rx","1.5px");
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	
	function changeDay(){
		console.log(timeline.dayselected,timeline.hourselected,timeline.minuteselected);
		$("input[name='online-checkbox']").bootstrapSwitch('state', false);
		let obj = {};
		obj.day = JSON.stringify(timeline.dayselected[0]);
		obj.hour = JSON.stringify(timeline.hourselected[0]);
		obj.minute = JSON.stringify(timeline.minuteselected[0]);
		$.ajax({
			type: 'GET',
			url: 'changeDay',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				timeline.timedata=evt_data;
				calcuTimeOpacity(selectedSOINN_tlind);
				inittimeline(timeline.selectedKey,timeline.selectedKey_color,timeline.selectedKey_color_sel)
				//init_legend();
				svg.selectAll("rect").attr("rx","1.5px");
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
		
	}

	function calcuTimeOpacity(timearr){
		//_.sortedIndex([10, 20, 30, 40, 50], 35);//3
		if(timearr==-1){return;}
		var daytime=_.pluck(timeline.timedata["day"],"tm")
		var hourtime=_.pluck(timeline.timedata["hour"],"tm")
		var minutetime=_.pluck(timeline.timedata["minute"],"tm")
		var daytimeind=[];
		var hourtimeind=[];
		var minutetimeind=[];
		var daytmpind=_.sortedIndex(daytime, timearr[0])-1;
		var hourtmpind=_.sortedIndex(hourtime, timearr[0])-1;
		var minutetmpind=_.sortedIndex(minutetime, timearr[0])-1;
		for(var i=0;i<timearr.length;i++){
			for(var j=daytmpind;j<daytime.length;j++){
				if(timearr[i]>=daytime[j] && timearr[i]<daytime[j]+86400){
					daytimeind.push(j);
					daytmpind=j+1;
					break;
				}
			}
			for(var j=hourtmpind;j<hourtime.length;j++){
				if(timearr[i]>=hourtime[j] && timearr[i]<hourtime[j]+3600){
					hourtimeind.push(j);
					hourtmpind=j+1;
					break;
				}
			}
			for(var j=minutetmpind;j<minutetime.length;j++){
				if(timearr[i]>=minutetime[j] && timearr[i]<minutetime[j]+60){
					minutetimeind.push(j);
					minutetmpind=j+1;
					break;
				}
			}
		}
		//console.log(daytimeind);
		//console.log(hourtimeind);
		//console.log(minutetimeind);
		daytimeind_hl=daytimeind;
		hourtimeind_hl=hourtimeind;
		minutetimeind_hl=minutetimeind;
	}
	function setTimeOpacity(){
		day_stack.attr("opacity",function(d,i){
			if(_.indexOf(daytimeind_hl,i,true)>=0){return 1;}
			else{return 0.3;}
		})
		hour_stack.attr("opacity",function(d,i){
			if(_.indexOf(hourtimeind_hl,i,true)>=0){return 1;}
			else{return 0.3;}
		})
		minute_stack.attr("opacity",function(d,i){
			if(_.indexOf(minutetimeind_hl,i,true)>=0){return 1;}
			else{return 0.3;}
		})
	}
	function resetHighlight(){
		selectedSOINN=-1;
		selectedSOINN_tlind=-1;
		daytimeind_hl=-1;hourtimeind_hl=-1;minutetimeind_hl=-1;
		day_stack.attr("opacity",1);
		hour_stack.attr("opacity",1);
		minute_stack.attr("opacity",1);
	}
	
	timeline.skiptime=function(newtime){
		timeline.curTime=newtime;
		var daydiffer=Math.floor((timeline.curTime-timeline.startTime)/(24*3600))
		var tmpDate=new Date(timeline.curTime*1000-8*60*60*1000);
		timeline.dayselected=[daydiffer];
		timeline.hourselected=[tmpDate.getHours()];
		timeline.minuteselected=[tmpDate.getMinutes()];
		resetHighlight();
		svg.selectAll("rect").attr("rx","1.5px");
		changeDay();
		//通知其他视图更新数据
		console.log("timerange",timeline.curTime,timeline.curTime+60);
		Observer.fireEvent("changeTimeRange_skip",[timeline.curTime,timeline.curTime+60],timeline);
	}
	
	$('input[name="timeline1"]').on('ifChecked', function(event){
	    var tmptl1=($(this).attr("id"));
	    tmptl1=tmptl1.split("_")[1]
	    curtype1=typecorr[tmptl1];
	    timeline.currentType=curtype1+curtype2;
		//console.log(timeline.currentType);
		changeType();
	});
	$('input[name="timeline2"]').on('ifChecked', function(event){
	    var tmptl2=($(this).attr("id"));
	    tmptl2=tmptl2.split("_")[1]
	    curtype2=typecorr[tmptl2];
	    timeline.currentType=curtype1+curtype2;
		//console.log(timeline.currentType);
		changeType();
	});
	
	$("input[name='online-checkbox']").on('switchChange.bootstrapSwitch', function (event,state) {  
        console.log(state);
		if(state){
			timeline.Interval=setInterval('timeline.updateByMinute()',timeline.Interval_time);
		}else{
			clearInterval(timeline.Interval); 
		}
    });  
	
	timeline.initdata=function(){
		$.ajax({
			type: 'GET',
			url: 'initTimeline',
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				//初始化
				timeline.timedata=evt_data;
				inittimeline(typelabelvar[timeline.currentType],typecolorvar[timeline.currentType],typecolor_selected_var[timeline.currentType])
				init_legend();
				svg.selectAll("rect").attr("rx","1.5px");
				//每Interval_time更新数据
				//timeline.Interval=setInterval('timeline.updateByMinute()',timeline.Interval_time);  
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	timeline.initdata();
	
	timeline.updateByMinute=function(){
		$.ajax({
			type: 'GET',
			url: 'updateByMinute',
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				timeline.curTime=timeline.curTime+60;
				//timeline.curTime_bak=timeline.curTime;
				var daydiffer=Math.floor((timeline.curTime-timeline.startTime)/(24*3600))
				var tmpDate=new Date(timeline.curTime*1000-8*60*60*1000);
				timeline.dayselected=[daydiffer];
				timeline.hourselected=[tmpDate.getHours()];
				timeline.minuteselected=[tmpDate.getMinutes()];
				console.log(timeline.dayselected,timeline.hourselected,timeline.minuteselected);
				
				resetHighlight();
				timeline.timedata=evt_data;
				inittimeline(timeline.selectedKey,timeline.selectedKey_color,timeline.selectedKey_color_sel)
				svg.selectAll("rect").attr("rx","1.5px");
				//通知其他视图更新数据
				console.log("timerange",timeline.curTime,timeline.curTime+60);
				Observer.fireEvent("updateMinute",[timeline.curTime,timeline.curTime+60],timeline);
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
				$("input[name='online-checkbox']").bootstrapSwitch('toggleState');
			},
		});
	}
	
	timeline.onMessage = function(message, data, from) {
        if (message == "selectSoinnNode") {
			console.log(data);
			resetHighlight();
			selectedSOINN=data;
			if(selectedSOINN!=-1){
				let obj = {};
				obj.type = JSON.stringify(selectedSOINN[0]);
				obj.nodeid = JSON.stringify(selectedSOINN[1]);
				//console.log(obj);
				$.ajax({
					type: 'GET',
					url: 'selectSoinnNode',
					data: obj,
					dataType: 'json',
					success: function(evt_data) {
						console.log(evt_data);
						selectedSOINN_tlind=evt_data.time;
						calcuTimeOpacity(selectedSOINN_tlind);
						setTimeOpacity();
					},
					error: function(jqXHR) {
						console.log('post error!!', jqXHR);
					},
				});
			}
        }
		if (message == "matrixClickTime") {
			if(data!=-1){timeline.skiptime(data);}
		}
    };
	
	
    Observer.addView(timeline);
    return timeline;
}
