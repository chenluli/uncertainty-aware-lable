function Soinn(Observer) {
    var soinn = {};
	
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
	 
	$("#soinn_wait").hide();
	
	var $bmDiv=$("#soinn");
    var width=$bmDiv.width();
    var height=$bmDiv.height();
	var padding=20;
	var svg=d3.select("#soinn")
			.append("svg")
			.attr("width", width)
			.attr("height", height).attr("class","soinn_svg");
	var $bmDiv2=$("#soinn_histogram");
    var width2=$bmDiv2.width();
    var height2=$bmDiv2.height();
	var svg2=d3.select("#soinn_histogram")
			.append("svg")
			.attr("width", width2)
			.attr("height", height2);
	var typetext;var labeltext;
	
	var nodecolor_normal=d3.interpolate(d3.rgb("#223442"),d3.rgb("#6cb7f5"));
	var nodecolor_abnormal=d3.interpolate(d3.rgb("#292118"),d3.rgb("#ffcc99"));
	
	soinn.linkdom = svg.append("g").attr("class", "links");
    soinn.nodedom = svg.append("g").attr("class", "nodes");
    soinn.nodedom_thre = svg.append("g").attr("class", "nodes_thre");
	soinn.labelednodes=[];
	soinn.nodedom_label = svg.append("g").attr("class", "nodes_labeled");
	
	soinn.nodehistoryrects = svg.append("g").attr("class", "nodehistoryrects");
	soinn.nodeaffects = svg.append("g").attr("class", "nodeaffects");
	
	soinn.clickedTlNodeID=-1;//点击的soinn节点
	soinn.lassoNodeID=-1;//圈选的soinn节点
	soinn.hightlightNodeID=-1;//高亮的soinn节点
	soinn.stackwinnum=-1;
	soinn.timefeatdata=-1;
	
	var node_r_scale; var link_width_scale;
	var x_scale; var y_scale;
	
	var totalnum=0;
	var labelednum=0;
	var normalnum=0;
	var abnormalnum=0;
	
	var normalthre=0.4;
	var abnormalthre=0.6;
	/*
	var randomarr=[];
	for(var i=0;i<65;){
		var tmpnum=parseInt(Math.random()*284, 10);
		if(_.indexOf(randomarr,tmpnum)<0){randomarr.push(tmpnum);i++;}
	}
	console.log(randomarr);
	*/
	
	
	
	function drawinfo(){
		//================nodes information================	
		//node types (uncertain normal abnormal)
		svg2.append("g").selectAll("circle").data([0,0,0])
			.enter().append("circle").attr("class","soinn_info_type")
			.attr("fill", function(d,i){
				var tmpcolor=["#c2c2c2",d3.rgb("#6cb7f5"),d3.rgb("#ffcc99")];
				return tmpcolor[i];
			})
			.attr("r", function(d,i){return 8;})
			.attr("cx", function(d,i){return 20+100*i;})
			.attr("cy", function(d,i){return height2/2;})
			.attr("stroke","white").attr("stroke-width",0)
			.on("click",function(d,i){
				if($(this).attr("stroke-width")==3){
					$(this).attr("stroke-width",0);
					soinn.hightlightNodeID=-1;
					hlnodes();
				}else{
					d3.selectAll(".soinn_info_type").attr("stroke-width",0);
					$(this).attr("stroke-width",3);
					soinn.hightlightNodeID=[];
					var tmptype=["uncertain","normal","abnormal"];
					for(var ii=0;ii<soinn.nodes.length;ii++){
						if(soinn.nodes[ii]["type"]==tmptype[i]){
							soinn.hightlightNodeID.push(ii);
						}
					}
					//console.log(soinn.hightlightNodeID);
					if(soinn.hightlightNodeID.length==0){soinn.hightlightNodeID=-1;}
					hlnodes();
					soinn.hightlightNodeID=-1;
				}
			});
		svg2.append("g").selectAll("text").data(["uncertain","normal","abnormal"])
			.enter().append("text")
			.text(function(d,i){return d;})
			.attr("x", function(d,i){return 40+100*i;})
			.attr("y", function(d,i){return height2/2-5;});			
		typetext=svg2.append("g").selectAll("text").data([soinn.nodes.length,0,0])
			.enter().append("text")
			.text(function(d,i){return d;})
			.attr("x", function(d,i){return 40+100*i;})
			.attr("y", function(d,i){return height2/2+10;});
		//node labeled (human labeled / computer labeled)
		var labelnodesg=svg2.append("g")
		labelnodesg.selectAll("circle").data([0,0])
			.enter().append("circle").attr("class","soinn_info_label")
			.attr("fill", "#c2c2c2")
			.attr("r", function(d,i){return 8;})
			.attr("cx", function(d,i){return 20+350+100*i;})
			.attr("cy", function(d,i){return height2/2;})
			.attr("stroke","white").attr("stroke-width",0)
			.on("click",function(d,i){
				if($(this).attr("stroke-width")==3){
					$(this).attr("stroke-width",0);
					soinn.hightlightNodeID=-1;
					hlnodes();
				}else{
					d3.selectAll(".soinn_info_label").attr("stroke-width",0);
					$(this).attr("stroke-width",3);
					soinn.hightlightNodeID=[];
					var tmptype=[1,0];
					for(var ii=0;ii<soinn.nodes.length;ii++){
						if(soinn.nodes[ii]["labeled"]==tmptype[i]){
							soinn.hightlightNodeID.push(ii);
						}
					}
					hlnodes();
					soinn.hightlightNodeID=-1;
				}
			});
		labelnodesg.append("circle")
			.attr("fill", "black")
			.attr("r", function(d,i){return 3;})
			.attr("cx", function(d,i){return 20+350+100*i;})
			.attr("cy", function(d,i){return height2/2;});
		svg2.append("g").selectAll("text").data(["labeled","unlabeled"])
			.enter().append("text")
			.text(function(d,i){return d;})
			.attr("x", function(d,i){return 40+350+100*i;})
			.attr("y", function(d,i){return height2/2-5;});			
		labeltext=svg2.append("g").selectAll("text").data([0,soinn.nodes.length])
			.enter().append("text")
			.text(function(d,i){return d;})
			.attr("x", function(d,i){return 40+350+100*i;})
			.attr("y", function(d,i){return height2/2+10;});
	}
	function updateinfo(){
		labelednum=0;
		normalnum=0;
		abnormalnum=0;
		for(var i=0;i<soinn.nodes.length;i++){
			if(soinn.nodes[i]["type"]=="normal"){
				normalnum=normalnum+1
			}else{
				if(soinn.nodes[i]["type"]=="abnormal"){abnormalnum=abnormalnum+1}
			}
			if(soinn.nodes[i]["labeled"]==1){
				labelednum=labelednum+1
			}
		}
		typetext.data([soinn.nodes.length-normalnum-abnormalnum,normalnum,abnormalnum])
			.text(function(d,i){return d;});
		labeltext.data([labelednum,soinn.nodes.length-labelednum])
			.text(function(d,i){return d;})
	}
	function setscale(){
		//==============scale=================
		var linkcnt=_.pluck(soinn.links,"cnt");
		var nodewinnum=_.pluck(soinn.nodes,"wincnt");
		var nodethre=_.pluck(soinn.nodes,"threshold");
		var feature=_.pluck(soinn.nodes,"feature");
		var featurexmax=_.max(feature, function(f){ return f[0]; })[0];
		var featurexmin=_.min(feature, function(f){ return f[0]; })[0];
		var featureymax=_.max(feature, function(f){ return f[1]; })[1];
		var featureymin=_.min(feature, function(f){ return f[1]; })[1];
		
		node_r_scale = d3.scaleSqrt().range([4,12]).domain([_.min(nodewinnum),_.max(nodewinnum)]);
		//var node_thre_scale = d3.scaleSqrt().range([6,15]).domain([0,_.max(nodethre)]);
		link_width_scale = d3.scaleLog().range([0.5,4]).domain([_.min(linkcnt),_.max(linkcnt)]);
		
		x_scale = d3.scaleLinear().range([padding,width-padding]).domain([featurexmin,featurexmax]);
		y_scale = d3.scaleLinear().range([padding,height-padding]).domain([featureymin,featureymax]);
		
	}
	var historytimer;
	
	
	
	function drawgraph(){
		
		//=================draw nodes================	
		soinn.nodedom.selectAll("circle").remove();
		var circles=soinn.nodedom.selectAll("circle").data(soinn.nodes)
			.enter().append("circle").attr("id",function(d,i){return "nodes_"+d.id;})
			.attr("fill", function(d){
				//if (d.type=="uncertain"){return "#c2c2c2";}
				if(d["certainty"][2]==1){return "#c2c2c2";}
				if (d.type=="normal" || (d["certainty"][0]>d["certainty"][1])){return nodecolor_normal(d["certainty"][0]);}
				if (d.type=="abnormal" || (d["certainty"][1]>d["certainty"][0])){return nodecolor_abnormal(d["certainty"][1]);}
			}).on("mousedown",function(d){
				//console.log(d3.event);
				if(d3.event.button==0){
					//左击
					console.log(d);
					soinn.nodeaffects.selectAll(".arc").remove();
					soinn.nodehistoryrects.selectAll("rect").remove();
					if(d.id==soinn.clickedTlNodeID){
						Observer.fireEvent("selectSoinnNode",-1,soinn);
						resetHightlight();
						
					}else{
						Observer.fireEvent("selectSoinnNode",[d.type,d.id],soinn);
						soinn.clickedTlNodeID=d.id;
						$(".soinn_svg .nodes circle").css("stroke-width",1);
						$(this).css("stroke-width",3);
						
						//获取影响节点
						var obj={};
						obj.nodeid = JSON.stringify(d.id);
						obj.labelednodes = JSON.stringify(soinn.labelednodes);
						console.log(obj);
						$.ajax({
							type: 'GET',
							url: 'nodeAffect',
							data: obj,
							dataType: 'json',
							success: function(evt_data) {
								console.log(evt_data);
								if(evt_data.affectnodes.length>0){
									//add pie
									drawaffectpie(d.id,evt_data.affectnodes,d3.select("#nodes_"+d.id).attr("cx"),d3.select("#nodes_"+d.id).attr("cy"),d3.select("#nodes_"+d.id).attr("r"));
								}
							},
							error: function(jqXHR) {
								console.log('post error!!', jqXHR);
							},
						});
						if(soinn.labelednodes.length>0){
							console.log("soinn node history "+d.id);
							//console.log(d3.select("#nodes_"+d.id).attr("cx"));
							var obj={};
							obj.nodeid = JSON.stringify(d.id);
							$.ajax({
								type: 'GET',
								url: 'getHistory',
								data: obj,
								dataType: 'json',
								success: function(evt_data) {
									console.log(evt_data);
									drawhistoryrects(d.id,evt_data["history"],d3.select("#nodes_"+d.id).attr("cx"),d3.select("#nodes_"+d.id).attr("cy"),d3.select("#nodes_"+d.id).attr("r"));
								},
								error: function(jqXHR) {
									console.log('post error!!', jqXHR);
								},
							});
						}
					}
				}else{
					//右击
					soinn.lassoNodeID=d.id;
					$(".soinn_svg .nodes circle").css("stroke-width",1);
					$(this).css("stroke-width",3);
				}
			})
			.attr("stroke",function(d,i){
				//if(_.indexOf(randomarr,d.id)>=0){return "green";}
				//if(_.indexOf([4,17,21,71,72,73,74,75,76,77,78,79,80,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181],d.id)>=0){
				if(_.indexOf(soinn.changednodes,d.id)>=0){
					return "#EE3B3B";
				}else{return "white";}
			})
			//.attr("id",function(d,i){return "soinnnode_"+d.id;})
			.attr("r", function(d,i){return node_r_scale(d.wincnt);})
			.attr("cx", function(d,i){return x_scale(d.feature[0]);})
			.attr("cy", function(d,i){return y_scale(d.feature[1]);});
		circles.append("title")
			  .text(function(d) {
				  var tmpcert=_.map(d.certainty, function(num){ return parseFloat(num.toFixed(2)); });
				  return d.id+" threshold:"+d.threshold.toFixed(2)+" wincnt:"+d.wincnt+" "+tmpcert; 
			  });	
		//=================draw links================	
		soinn.linkdom.selectAll("line").remove();
		soinn.linkdom.selectAll("line").data(soinn.links)
			.enter().append("line")
			.attr("x1", function(d){return x_scale(soinn.nodes[d.source].feature[0]);})
			.attr("y1", function(d){return y_scale(soinn.nodes[d.source].feature[1]);})
			.attr("x2", function(d){return x_scale(soinn.nodes[d.target].feature[0]);})
			.attr("y2", function(d){return y_scale(soinn.nodes[d.target].feature[1]);})
			.attr("stroke","white")
			.attr("stroke-width", function(d){return link_width_scale(d.cnt);})
			.on("click",function(d){
				console.log(d);
			});
		//=================draw labeled mark================	
		soinn.nodedom_label.selectAll("circle").remove();
		soinn.nodedom_label.selectAll("circle").data(soinn.labelednodes)
			.enter().append("circle")
			.attr("fill","black").attr("r",3)
			.attr("cx", function(d){
				return x_scale(soinn.nodes[d["id"]].feature[0]);
			})
			.attr("cy", function(d){
				return y_scale(soinn.nodes[d["id"]].feature[1]);
			});
		//=================right click nodes================	
		$.contextMenu({
            selector: ("#soinn svg .nodes circle"), 
            callback: function(key, options) {
				if(key=="normal"){
					labelnode("normal",soinn.lassoNodeID);
				}else{
					if(key=="abnormal"){
						labelnode("abnormal",soinn.lassoNodeID);
					}
				}
				resetHightlight();
            },
            items: {
                "normal": {name: "Normal"},
                "abnormal": {name: "Abnormal"},
                "cancel": {name: "Cancel"}
            }
        });
		svg.on("mouseup",function(){
			if(event.target.nodeName=="svg"){
				resetHightlight();
				Observer.fireEvent("selectSoinnNode",-1,soinn);
			}
		});
	}
	function drawaffectpie(clickedid,affectnode,x,y,r){
		x=parseInt(x);
		y=parseInt(y);
		r=parseInt(r);
		var sortedaffected=_.sortBy(affectnode, function(d){ return -d[1]; });
		var tmptotal=0;
		var newaffected=[];
		for(var i=0;i<5;i++){
			newaffected.push(sortedaffected[i]);
			tmptotal=tmptotal+sortedaffected[i][1];
			if(tmptotal>0.9){
				break;
			}
		}
		console.log(affectnode);
		console.log(sortedaffected);
		console.log(newaffected);
		
		var pie = d3.pie()
			.sort(null)
			.value(function(d) { return d[1]; });

		var path = d3.arc()
			.outerRadius(r+17)
			.innerRadius(r+8);
			
		soinn.nodeaffects.selectAll(".arc").data(pie(newaffected))
			.enter().append("g").attr("class", "arc")
			.attr("transform", "translate(" + x + "," + y + ")")
			.append("path")
			.attr("d", path)
			.attr("fill", function(d) {return d3.select("#nodes_"+d.data[0]).attr("fill"); })
			.attr("stroke","white")
			.attr("stroke-width", 3)
			.on("mouseover",function(d){
				//console.log(d.data);
				soinn.nodedom.selectAll("circle").attr("opacity",0.2);
				soinn.linkdom.selectAll("line").attr("opacity",0.2);
				d3.select("#nodes_"+clickedid).attr("opacity",1);
				d3.select("#nodes_"+d.data[0]).attr("opacity",1);
			}).on("mouseout",function(){
				soinn.nodedom.selectAll("circle").attr("opacity",1);
				soinn.linkdom.selectAll("line").attr("opacity",1);
			});
	}
	
	function drawhistoryrects(clickedid,histdata,x,y,r){
		//soinn.nodehistoryrects.selectAll("rect").remove();
		//console.log(x,y,r);
		x=parseInt(x);
		y=parseInt(y);
		r=parseInt(r);
		var num=histdata.length;
		var rectwh=10;
		soinn.nodehistoryrects.selectAll("rect").data(histdata)
			.enter().append("rect")
			.attr("fill", function(d){
				if(d[2]==1){return "#c2c2c2";}
				if (d[0]>normalthre || (d[0]>d[1])){return nodecolor_normal(d[0]);}
				if (d[1]>abnormalthre || (d[1]>d[0])){return nodecolor_abnormal(d[1]);}
			})
			.attr("x", function(d,i){
				return x-rectwh*num/2+rectwh*i;
			})
			.attr("y", y-r-35)
			.attr("width", rectwh).attr("height", rectwh)
			.attr("stroke","white")
			.attr("stroke-width", 1.5).attr("rx",1).attr("ry",1)
			.on("mouseover",function(d,i){
				//console.log(d.data);
				soinn.nodedom.selectAll("circle").attr("opacity",0.2);
				soinn.linkdom.selectAll("line").attr("opacity",0.2);
				d3.select("#nodes_"+clickedid).attr("opacity",1);
				d3.select("#nodes_"+soinn.labelednodes[i]["id"]).attr("opacity",1);
			}).on("mouseout",function(){
				soinn.nodedom.selectAll("circle").attr("opacity",1);
				soinn.linkdom.selectAll("line").attr("opacity",1);
			});
	}
	
	function hlnodes(){
		//响应高亮
		soinn.nodedom.selectAll("circle").attr("opacity",1);
		soinn.linkdom.selectAll("line").attr("opacity",1);
		soinn.nodedom_label.selectAll("circle").attr("opacity",1);
		if(soinn.hightlightNodeID!=-1 && soinn.hightlightNodeID.length!=0){
			soinn.nodedom.selectAll("circle").filter(function(d) { 
					return _.indexOf(soinn.hightlightNodeID,d.id)<0; 
				})
				//.transition()
				//.duration(1000)
				.attr("opacity",0.2);
			soinn.linkdom.selectAll("line").filter(function(d) { 
					return _.indexOf(soinn.hightlightNodeID,d.source)<0 || _.indexOf(soinn.hightlightNodeID,d.target)<0; 
				}).attr("opacity",0.2);
			soinn.nodedom_label.selectAll("circle").filter(function(d) { 
					return _.indexOf(soinn.hightlightNodeID,d.id)<0; 
				}).attr("opacity",0.2);
		}
		
	}

	function labelnode(labeltype,nodeid){
		//右击标注节点
		if(nodeid!=-1){
			soinn.labelednodes.push({"id":nodeid,"type":labeltype});
			/*
			if(soinn.labelednodes.length==0){
				soinn.labelednodes.push({"id":nodeid,"type":labeltype});
			}
			else{
				var i=0
				for(;i<soinn.labelednodes.length;i++){
					if(soinn.labelednodes[i]["id"]==nodeid){
						soinn.labelednodes[i]["type"]=labeltype;
						break;
					}
				}
				if(i==soinn.labelednodes.length){
					soinn.labelednodes.push({"id":nodeid,"type":labeltype});
				}
			}
			*/
		}
		
		let obj = {};
		//console.log(normal0ab1,soinn.lassoNodeID_normal,soinn.lassoNodeID_abnormal);
		//obj.labelednodes = JSON.stringify(soinn.labelednodes);
		obj.labelednodes = JSON.stringify({"id":nodeid,"type":labeltype});
		obj.normalthre=JSON.stringify(normalthre);
		obj.abnormalthre=JSON.stringify(abnormalthre);
		console.log(obj);
		$("#soinn_wait").show(function(){
			var target= document.getElementById('soinn_wait');
			spinner.spin(target);  
		});
		$.ajax({
			type: 'GET',
			url: 'labelSoinn',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				Observer.fireEvent("re_initmatrix",nodeid,matrix);
				console.log(evt_data);
				//totalinit(evt_data);
				//getchangednodes(soinn.nodes,evt_data.nodes);
				soinn.nodes=evt_data.nodes;
				soinn.changednodes=evt_data.changednodes;
				var tmplabeledid=_.pluck(soinn.labelednodes,"id");
				soinn.labelednodes=_.without(soinn.labelednodes, tmplabeledid);
				updateinfo();
				drawgraph();
				/*
				var tmpcertainty=_.pluck(soinn.nodes,"certainty");
				var tt=_.sortBy(tmpcertainty, function(d){ return d[0]; });
				var ttt=_.sortBy(tmpcertainty, function(d){ return d[1]; });
				console.log("normal");console.log(tt);
				console.log("abnormal");console.log(ttt);
				*/
				$("#soinn_wait").hide();
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	soinn.resetlayout=function(){
		$.ajax({
			type: 'GET',
			url: 'resetLayout',
			//data: obj,
			dataType: 'json',
			success: function(evt_data) {
				soinn.nodes=evt_data.nodes;
				soinn.links=evt_data.links;
				soinn.distance=evt_data.distance;
				soinn.labelednodes=[];
				totalnum=soinn.nodes.length;
				for(var i=0;i<totalnum;i++){
					if(soinn.nodes[i]["labeled"]==1){
						soinn.labelednodes.push({"id":i,"type":soinn.nodes[i]["type"]});
					}
				}
				updateinfo();
				setscale();
				drawgraph();
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	soinn.initgraph=function(){
		$.ajax({
			type: 'GET',
			url: 'init_soinn',
			dataType: 'json',
			success: function(evt_data) {
				soinn.nodes=evt_data.nodes;
				soinn.links=evt_data.links;
				soinn.changednodes=evt_data.changednodes;
				//soinn.timematchnode=evt_data.match;
				soinn.distance=evt_data.distance;
				totalnum=soinn.nodes.length;
				/*
				soinn.labelednodes=[];
				for(var i=0;i<totalnum;i++){
					if(soinn.nodes[i]["labeled"]==1){
						soinn.labelednodes.push({"id":i,"type":soinn.nodes[i]["type"]});
					}
				}
				*/
				soinn.labelednodes=evt_data.labelednode;
				var tmplabeledid=_.pluck(soinn.labelednodes,"id");
				soinn.labelednodes=_.without(soinn.labelednodes, tmplabeledid);
				console.log(evt_data);
				drawinfo();
				updateinfo();
				setscale();
				drawgraph();
				//drawgraph_force();
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	soinn.initgraph();
	function resetHightlight(){
		soinn.clickedTlNodeID=-1;
		soinn.lassoNodeID=-1;
		soinn.hightlightNodeID=-1;
		soinn.stackwinnum=-1;
		
		$(".soinn_svg .nodes circle").css("stroke-width",1);
		$(".soinn_svg circle").attr("opacity",1);
		$(".soinn_svg line").attr("opacity",1);
		d3.selectAll(".soinn_info_type").attr("stroke-width",0);
		d3.selectAll(".soinn_info_label").attr("stroke-width",0);
		soinn.nodeaffects.selectAll(".arc").remove();
		soinn.nodehistoryrects.selectAll("rect").remove();
	}
	
    soinn.onMessage = function(message, data, from) {
    	//console.log(message)
        if (message == "hlSoinnNode") {
			if(data==-1){soinn.hightlightNodeID=-1}
			else{soinn.hightlightNodeID=[data];}
			hlnodes();
        }
		if (message == "changeTimeRange" || message == "changeTimeRange_skip") {
			resetHightlight();
			
			let obj = {};
			obj.starttime = JSON.stringify(data[0]);
			obj.endtime = JSON.stringify(data[1]);
			//console.log(obj);
			$.ajax({
				type: 'GET',
				url: 'filterSoinnNode',
				data: obj,
				dataType: 'json',
				success: function(evt_data) {
					console.log(evt_data);
					//soinn.timefeatdata=evt_data;
					soinn.hightlightNodeID=[];
					for(var i=0;i<evt_data.nodes.length;i++){
						for(var j=0;j<evt_data.nodes[i].length;j++){
							var tmpid=parseInt(evt_data.nodes[i][j].split("_")[1]);
							soinn.hightlightNodeID.push(tmpid);
						}
					}
					soinn.hightlightNodeID=_.uniq(soinn.hightlightNodeID);
					console.log(soinn.hightlightNodeID);
					hlnodes();
				},
				error: function(jqXHR) {
					console.log('post error!!', jqXHR);
				},
			});
			
        }
		if (message == "updateSoinn_start"){
			$("#soinn_wait").show(function(){
				var target= document.getElementById('soinn_wait');
				spinner.spin(target);  
			});
		}
		if (message == "updateSoinn") {
			resetHightlight();
			$.ajax({
				type: 'GET',
				url: 'init_soinn',
				dataType: 'json',
				success: function(evt_data) {
					soinn.nodes=evt_data.nodes;
					soinn.links=evt_data.links;
					soinn.distance=evt_data.distance;
					soinn.labelednodes=[];
					totalnum=soinn.nodes.length;
					for(var i=0;i<totalnum;i++){
						if(soinn.nodes[i]["labeled"]==1){
							soinn.labelednodes.push({"id":i,"type":soinn.nodes[i]["type"]});
						}
					}
					setscale();
					labelnode(-1,-1);
					Observer.fireEvent("updateSoinn_end",[],matrix);
					//$("#soinn_wait").hide();
				},
				error: function(jqXHR) {
					console.log('post error!!', jqXHR);
				},
			});
        }
    };
	
	
	
    Observer.addView(soinn);
    return soinn;

}