
function Netforce(Observer){
	var netforce={};
	
	var $brtDiv=$("#top-right-top-div");
    width=$brtDiv.width();
    height=$brtDiv.height();
	var graphWidth=width;
	var graphHeight=height;
	var WHrate = Math.sqrt(graphWidth * graphHeight / 1200/ 400);
	
	var svg=d3.select("#netforce_view")
			.append("svg")
			.attr("width", width)
			.attr("height", height);
	var svg_g = svg.append("g");
        //background
    svg_g.append("g").attr("class", "bg").append("rect")
            .attr("width", graphWidth)
            .attr("height", graphHeight)
            .attr("x", 0).attr("y", 0)
            .attr("fill", "white")
            .attr("opacity", 0);
			
	//var colorarr=[d3.rgb("#292118"),d3.rgb("#ffcc99")];
	var linkdom = svg_g.append("g").attr("class", "links").selectAll("line");
    var nodedom = svg_g.append("g").attr("class", "nodes").selectAll("rect");
	
	
	var curTime=Observer.starttime;
	
	var currentZoom = 1;
    var currentTran = [0, 0];
	
	var nodedata;var linkdata;
	var alliparr;
	var selectedip=[];//click的ip
	var selectedip_linked=[];//和click的ip相连接的ip
	var hliparr=[];//收到要高亮的ip
	var hliparr_linked=[];//和收到要高亮的ip相连接的ip
	
	//var node_r_scale = d3.scaleLog().range([1,6]).domain([(_.min(nodeallbtyes)+1),(_.max(nodeallbtyes)+1)]);
	var spectialIP={"Adm":[2886336552],"dc":[2886336514,2886991874,2887647234],
		"SMTP":[2886336515,2886991875,2887647235],
		"HTTP":[
			2886336516,2886336517,2886336519,2886336520,2886336521,
			2886991876,2886991877,2886991878,2886991879,2886991880,
			2887647236,2887647237,2887647238,2887647239,2887647240
		],"WSS":[]};
	var spectialIPcolor=["#DB7093","#EEE685","#9BCD9B","#C6E2FF","#003366"];
	var spectialIPKey=_.keys(spectialIP);
	var minwh=4;
	var node_width = d3.scaleLinear().range([8,15]);
	var node_height = d3.scaleLinear().range([8,15]);
	var node_width_f=function(d){if(d==0){return minwh;}else{return node_width(d);}}
	var node_height_f=function(d){if(d==0){return minwh;}else{return node_height(d);}}
	var link_width_scale = d3.scaleLog().range([0.5,4]);
	var link_strength = d3.scaleLinear().range([0.5,1]);
	var link_dis = d3.scaleLinear().range([55,5]);
	var nodecolor=function(d){
		for(var i=0;i<spectialIPKey.length;i++){
			if(_.indexOf(spectialIP[spectialIPKey[i]],d)>=0){
				return spectialIPcolor[i];
			}
		}
		var tmpip=Observer.int2iP(d);
		if(tmpip.split(".")[0]=="172"){return spectialIPcolor[spectialIPcolor.length-1];}
		return "#663300";
	}
	//d3.interpolate(colorarr[0],colorarr[1]);
	
	var simulation= d3.forceSimulation()
					.force("x", d3.forceX(graphWidth / 2).strength(Math.min(0.7, 0.1 * 1300 / graphWidth)))
					.force("y", d3.forceY(graphHeight / 2).strength(Math.min(0.7, 0.3 * 500 / graphHeight)))
					.force("center", d3.forceCenter(graphWidth / 2, graphHeight / 2))
					.on("tick",ticked).stop();
	function ticked() {
		nodedom.attr("x", function(d) { return d.x-node_width_f((d.src))/2; })
			.attr("y", function(d) { return d.y-node_height_f((d.dst))/2; });
		linkdom.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	}
	function dragstarted(d) {
		if (!d3.event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}
	function dragged(d) {
		d.fx = d3.event.x;
		d.fy = d3.event.y;
	}

	function dragended(d) {
		if (!d3.event.active) simulation.alphaTarget(0);
		//calcuNodesInfo();
	}
	//zoom
	var zoomHandler = function() {
		currentZoom = d3.event.transform.k;
		// limit translation to thresholds
		var tbound = -graphHeight * currentZoom,
			bbound = graphHeight * currentZoom,
			lbound = -graphWidth * currentZoom,
			rbound = graphWidth * currentZoom;
		var translation = d3.event ? [d3.event.transform.x, d3.event.transform.y] : [0, 0];
		translation = [
			Math.max(Math.min(translation[0], rbound), lbound),
			Math.max(Math.min(translation[1], bbound), tbound)
		];
		currentTran = translation;
		svg_g.attr("transform", "translate(" + translation + ")" + " scale(" + currentZoom + ")");
	};
	var zoom = d3.zoom()
		.scaleExtent([1, 10])
		.translateExtent([
			[0, 0],
			[graphWidth, graphHeight]
		])
		.extent([
			[0, 0],
			[graphWidth, graphHeight]
		])
		.on("zoom", zoomHandler)
		.on("end", function() {
			if (currentZoom > 1) { svg.attr("cursor", "move"); } else { svg.attr("cursor", "default"); }
		});
	svg.call(zoom);
	
	
	var formatname=["G","M","K","B"];
	var tiptool = d3.tip()
			.attr('class', 'd3-tip forcetip')
			.html(function(d,i){return bytetip(d);})
			.offset([-10, 0]);
	function bytetip(d){
		var t=(d.src+d.dst+1); 
		var format=1e9;
		var formatcnt=0;
		while(t/format<1){format=format/1000;formatcnt++;}
		t=t/format;t=t.toFixed(2);
		var tmpip=Observer.int2iP(d.ip);
		return "<strong>IP:</strong> <span style='color:red'>" +tmpip +"</span>"+
			"&nbsp;&nbsp;<strong>src:</strong> <span style='color:red'>" + (d.src/format).toFixed(2)+formatname[formatcnt]+"</span>"+
			"&nbsp;&nbsp;<strong>dst:</strong> <span style='color:red'>" + (d.dst/format).toFixed(2)+formatname[formatcnt]+"</span>";
	}
	svg.call(tiptool);
		
	function resetgraph(starttime,endtime){
		let obj = {};
		obj.starttime=JSON.stringify(starttime);
		obj.endtime=JSON.stringify(endtime);
		$.ajax({
			type: 'GET',
			url: 'forcedata',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				nodedata=evt_data.nodes;
				linkdata=evt_data.links;
				alliparr=_.pluck(evt_data.nodes,"ip");
				initlayout(nodedata,linkdata);
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
		
	}
	resetgraph(curTime,curTime+60);
	drawlabel();
	
	
	function drawlabel(){
		var legendw=svg.append("g").attr("class", "labeltext");
		legendw.append("line")
			.attr("x1",25).attr("x2",45)
			.attr("y1",20).attr("y2",20);
		legendw.append("line")
			.attr("x1",25).attr("x2",25)
			.attr("y1",20).attr("y2",40);
		legendw.append("text")
			.attr("x", 25).attr("y", 14).text("src");
		legendw.append("text")
			.attr("x", -40).attr("y", 15).text("dst").attr("transform","rotate(-90)");
		
		var legend = svg.append("g").attr("class", "labeltext")
			.selectAll("g")
			.data(spectialIPKey)
			.enter().append("g")
			.attr("transform", function(d, i) { return "translate("+(60+25*i)+"," + 15 + ")"; });
		legend.append("circle")
			.attr("cx", function(d,i){return 10+30*i;})
			.attr("cy", 10)
			.attr("r",5)
			.attr("fill",function(d,i){return spectialIPcolor[i];})
		var text=["dstip","srcip"];
		legend.append("text")
			.attr("x", function(d,i){return 20+30*i;})
			.attr("y", 12.5)
			.text(function(d,i) {;return d; });
	}
	function initlayout(datanode,datalink){
		//==============scale=================
		var linkcnt=_.pluck(datalink,"cnt");

		var nodesrcbtyes=_.pluck(datanode,"src");
		var nodedstbtyes=_.pluck(datanode,"dst");
		var [ ...nodeallbtyes ] = nodesrcbtyes;
		for(var i=0;i<nodeallbtyes.length;i++){
			nodeallbtyes[i]=nodeallbtyes[i]+nodedstbtyes[i];
		}
		node_width.domain([(_.min(nodesrcbtyes)+1),(_.max(nodesrcbtyes)+1)]);
		node_height.domain([(_.min(nodedstbtyes)+1),(_.max(nodedstbtyes)+1)]);
		link_width_scale.domain([_.min(linkcnt),_.max(linkcnt)]);
		link_strength.domain([_.min(linkcnt),_.max(linkcnt)]);
		link_dis.domain([_.min(linkcnt),_.max(linkcnt)]);
		//var node_color_scale = d3.scaleLinear().range([0,1]).domain([_.min(nodetime),_.max(nodetime)]);
		
		//==============simulation=================
		simulation.force("link", d3.forceLink().strength(function strength(link) {
						return link_strength(link.cnt);
					}).distance(function(d,i){return link_dis(d.cnt);}))
					.force("charge", d3.forceManyBody().strength(-400 * WHrate/Math.pow(datanode.length,0.9)*27.5));
		
		//=================update node================			
		nodedom = nodedom.data(datanode,function(d){return d;});//一定要返回d！
		nodedom.exit().transition().attr("r", 0).remove();
		var nodedom_new = nodedom.enter().append("rect")
			.attr("fill", function(d){
				return nodecolor(d.ip);
			})/*
			.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended))*/
			.attr("cursor", "pointer")
			.on("dblclick",function(d){
				d3.event.stopPropagation();
				//console.log(d);
				hliparr=[];
				var tmpind=_.indexOf(selectedip,d.ip);
				if(tmpind>=0){
					selectedip=_.without(selectedip,d.ip);
				}else{
					selectedip.push(d.ip);
					/*
					var iptype=[];
					for (var i=0;i<selectedip.length;i++){
						var tmpind=_.indexOf(alliparr,selectedip[i]);
						if(datanode[tmpind]["src"]>datanode[tmpind]["dst"]){
							iptype.push("src");
						}else{iptype.push("dst");}
					}
					*/
					var iptype;
					
					var tmpind=_.indexOf(alliparr,d.ip);
					if(datanode[tmpind]["src"]>datanode[tmpind]["dst"]){
						iptype="src";
					}else{iptype="dst";}
					
					Observer.fireEvent("showipbytes",[d.ip,iptype],netforce);
					/*
					var iptype=[];
					var tmpind=_.indexOf(alliparr,d.ip);
					if(datanode[tmpind]["src"]>datanode[tmpind]["dst"]){
						iptype.push("src");
					}else{iptype.push("dst");}
					Observer.fireEvent("showipbytes",[d.ip,iptype],netforce);
					*/
				}
				selectedip_linked=getlinkedip(selectedip);
				hlip(selectedip,selectedip_linked);
				console.log(selectedip);
				Observer.fireEvent("highlightip",selectedip,netforce);
				
				
			})
			.call(function(node) { node.transition().attr("width", function(d,i){
				return node_width_f((d.src));}).attr("height", function(d,i){
				return node_height_f((d.dst));}); 
			})
		//nodedom_new.append("title")
		//	  .text(function(d) {return "id:"+d.id+" ip:"+d.ip; });	
		nodedom=nodedom_new.merge(nodedom);

		//=================update link================	
		linkdom = linkdom.data(datalink,function(d){return d;});//一定要返回d！
		linkdom.exit().remove();
		linkdom = linkdom.enter().append("line")
			.attr("stroke","white")
			.call(function(link) { link.transition().attr("stroke-width", function(d){return link_width_scale(d.cnt);}); })
			.merge(linkdom);

		//=================restart simulation================	
		simulation.nodes(datanode);
		simulation.force("link").links(datalink);
		simulation.alpha(1).restart();
		
		//======================= tip ======================	
		
		nodedom.on('mouseover', tiptool.show)
			.on('mouseout', tiptool.hide);
	}
	function getlinkedip(iparr){
		var linked=[];
		for(var i=0;i<linkdata.length;i++){
			var tmpindsrc=_.indexOf(iparr,linkdata[i]["source"]["ip"]);
			var tmpinddst=_.indexOf(iparr,linkdata[i]["target"]["ip"]);
			if(tmpindsrc>=0 && tmpinddst<0){
				linked.push(linkdata[i]["target"]["ip"]);
			}
			if(tmpindsrc<0 && tmpinddst>=0){
				linked.push(linkdata[i]["source"]["ip"]);
			}
		}
		linked=_.uniq(linked);
		return linked;
		//console.log(selectedip);
		//console.log(selectedip_linked);
	}
	function hlip(iparr,linkediparr){
		if(iparr.length==0){
			nodedom.attr("opacity",1).attr("class",null);
			linkdom.attr("opacity",1);
			return;
		}
		nodedom.attr("opacity",function(d){
				if(_.indexOf(linkediparr,d.ip)>=0||_.indexOf(iparr,d.ip)>=0){return 1;}
				else{return 0.2;}
			}).attr("class",function(d){
				if(_.indexOf(iparr,d.ip)>=0){return "hlip";}
				else{return null;}
			})
		linkdom.attr("opacity",function(d){
				if((_.indexOf(iparr,d.source.ip)>=0 || _.indexOf(linkediparr,d.source.ip)>=0) 
					&& (_.indexOf(iparr,d.target.ip)>=0 || _.indexOf(linkediparr,d.target.ip)>=0))
					{return 1;}
				else{return 0.2;}
			})
	}
	
    netforce.onMessage = function(message, data, from){
		//console.log(from); 
		if(message == "changeTimeRange" || message == "updateMinute" || message == "changeTimeRange_skip"){
			curTime=data[0];
			resetgraph(data[0],data[1]);
		}
		if(message=="highlightip" && from!=netforce){
			selectedip=[];
			selectedip_linked=[]
			hliparr=data;
			hliparr_linked=getlinkedip(hliparr);
			hlip(hliparr,hliparr_linked);
		}
		
	}
	
	
	Observer.addView(netforce);
	return netforce;
}
	
	
