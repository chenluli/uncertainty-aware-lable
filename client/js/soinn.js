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
	soinn.nodedom_label = svg.append("g").attr("class", "nodes_labeled");
	
	soinn.clickedTlNodeID=-1;//点击的soinn节点
	soinn.lassoNodeID=-1;//圈选的soinn节点
	soinn.hightlightNodeID=-1;//高亮的soinn节点
	soinn.stackwinnum=-1;
	soinn.timefeatdata=-1;
	
	
	function drawgraph(){
		//==============scale=================
		var linkcnt=_.pluck(soinn.links,"cnt");
		var nodewinnum=_.pluck(soinn.nodes,"wincnt");
		var nodethre=_.pluck(soinn.nodes,"threshold");
		var feature=_.pluck(soinn.nodes,"feature");
		var featurexmax=_.max(feature, function(f){ return f[0]; })[0];
		var featurexmin=_.min(feature, function(f){ return f[0]; })[0];
		var featureymax=_.max(feature, function(f){ return f[1]; })[1];
		var featureymin=_.min(feature, function(f){ return f[1]; })[1];
		
		var node_r_scale = d3.scaleSqrt().range([4,12]).domain([_.min(nodewinnum),_.max(nodewinnum)]);
		var node_thre_scale = d3.scaleSqrt().range([6,15]).domain([0,_.max(nodethre)]);
		var link_width_scale = d3.scaleLog().range([0.5,4]).domain([_.min(linkcnt),_.max(linkcnt)]);
		
		var x_scale = d3.scaleLinear().range([padding,width-padding]).domain([featurexmin,featurexmax]);
		var y_scale = d3.scaleLinear().range([padding,height-padding]).domain([featureymin,featureymax]);
		
		//=================draw nodes================	
		soinn.nodedom.selectAll("circle").remove();
		var circles=soinn.nodedom.selectAll("circle").data(soinn.nodes)
			.enter().append("circle")//.attr("class","soinn_nodes")
			.attr("fill", function(d){
				if (d.type=="uncertain"){return "grey";}
				if (d.type=="normal"){return d3.rgb("#6cb7f5");}
				if (d.type=="abnormal"){return d3.rgb("#ffcc99");}
			}).on("mousedown",function(d){
				//console.log(d3.event);
				if(d3.event.button==0){
					//左击
					console.log(d);
					if(d.id==soinn.clickedTlNodeID){
						Observer.fireEvent("selectSoinnNode",-1,soinn);
						resetHightlight();
					}else{
						Observer.fireEvent("selectSoinnNode",[d.type,d.id],soinn);
						soinn.clickedTlNodeID=d.id;
						$(".soinn_svg .nodes circle").css("stroke-width",0.5);
						$(this).css("stroke-width",3);
						
					}
				}else{
					//右击
					soinn.lassoNodeID=d.id;
					$(this).css("stroke-width",3);
				}
				
			})
			//.attr("id",function(d,i){return "soinnnode_"+d.id;})
			.attr("r", function(d,i){return node_r_scale(d.wincnt);})
			.attr("cx", function(d,i){return x_scale(d.feature[0]);})
			.attr("cy", function(d,i){return y_scale(d.feature[1]);});
		circles.append("title")
			  .text(function(d) {return d.id+" threshold:"+d.threshold.toFixed(2)+" wincnt:"+d.wincnt; });	
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
		
		//=================right click nodes================	
		$.contextMenu({
            selector: ("#soinn svg .nodes circle"), 
            callback: function(key, options) {
				if(key=="normal"){
					let obj = {};
					//console.log(normal0ab1,soinn.lassoNodeID_normal,soinn.lassoNodeID_abnormal);
					obj.type = JSON.stringify("normal");
					obj.nodes = JSON.stringify(soinn.lassoNodeID);
					console.log(obj);
					$("#soinn_wait").show(function(){
						var target= document.getElementById('soinn_wait');
						spinner.spin(target);  
					});
					$.ajax({
						type: 'GET',
						url: 'modifySoinn',
						data: obj,
						dataType: 'json',
						success: function(evt_data) {
							console.log(evt_data);
							//totalinit(evt_data);
							$("#soinn_wait").hide();
						},
						error: function(jqXHR) {
							console.log('post error!!', jqXHR);
						},
					});
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
		//================nodes information================	
		svg2.append("g").selectAll("circle").data([0,0,0])
			.enter().append("circle")
			.attr("fill", function(d,i){
				var tmpcolor=["grey",d3.rgb("#6cb7f5"),d3.rgb("#ffcc99")];
				return tmpcolor[i];
			})
			.attr("r", function(d,i){return 8;})
			.attr("cx", function(d,i){return 20+100*i;})
			.attr("cy", function(d,i){return height2/2;});
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
	}
	function hlnodes(){
		if(soinn.hightlightNodeID==-1){
			soinn.nodedom.selectAll("circle").attr("opacity",1);
			soinn.linkdom.selectAll("line").attr("opacity",1);
		}else{
			soinn.nodedom.selectAll("circle").filter(function(d) { 
					return _.indexOf(soinn.hightlightNodeID,d.id)<0; 
				})
				//.transition()
				//.duration(1000)
				.attr("opacity",0.2);
			soinn.linkdom.selectAll("line").filter(function(d) { 
					return _.indexOf(soinn.hightlightNodeID,d.source)<0 || _.indexOf(soinn.hightlightNodeID,d.target)<0; 
				}).attr("opacity",0.2);
		}
		
	}
	
	soinn.initgraph=function(){
		$.ajax({
			type: 'GET',
			url: 'init_soinn',
			dataType: 'json',
			success: function(evt_data) {
				soinn.nodes=evt_data.nodes;
				soinn.links=evt_data.links;
				console.log(evt_data);
				drawgraph();
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
		
		$(".soinn_svg .nodes circle").css("stroke-width",0.5);
		$(".soinn_svg circle").attr("opacity",1);
		$(".soinn_svg line").attr("opacity",1);
		
	}
	
    soinn.onMessage = function(message, data, from) {
    	//console.log(message)
        if (message == "updateMinute") {
			
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
    };
	
	
	
    Observer.addView(soinn);
    return soinn;

}