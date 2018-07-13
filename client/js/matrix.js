
function Matrix(Observer){
	var matrix={};
	
	var $brtDiv=$("#matrix");
    var width=$brtDiv.width();
	var width_bak=width;
    var height=$brtDiv.height();
	var height_bak=height;
	var lefttextw=20;
	var noderadius=8;
	var toptexth=20;
	var timesliceh=20;
	var timeslicew=10;
	var matrixw=20;var matrixh=25;
	var margin = {top: toptexth+timesliceh+15, right: 20, bottom: 20, left: lefttextw+noderadius*2+15};
	
	var svg=d3.select("#matrix")
			.append("svg")
			.attr("width", width)
			.attr("height", height).attr("class","matrix_svg");
	
	matrix.nodedom = svg.append("g").attr("class", "matrixnodes");
	matrix.nodedom_label = svg.append("g").attr("class", "nodes_labeled");
	matrix.timedom = svg.append("g").attr("class", "times");
	matrix.matrixdom = svg.append("g").attr("class", "matrix_matrix");
	
	var nodecolor_normal=d3.interpolate(d3.rgb("#223442"),d3.rgb("#6cb7f5"));
	var nodecolor_abnormal=d3.interpolate(d3.rgb("#292118"),d3.rgb("#ffcc99"));
	var nodecolor_uncertain=d3.interpolate(d3.rgb("#5e5e5e"),d3.rgb("#e0e0e0"));
	
	matrix.clickedTlNodeID=-1;
	matrix.clickedTlTime=-1;
	matrix.labeledTimeind=-1;
	//matrix.hightlightNodeID=-1;
	
	var nodestype=["normal","abnormal","uncertain"];
	
	function drawmatrix(){
		//======================adjust w h===========================
		var tmpw=(width_bak-margin.left-margin.right)/matrix.timearr.length;
		if(tmpw>20){matrixw=tmpw;width=width_bak;}
		else{matrixw=20;width=margin.left+matrixw*matrix.timearr.length+margin.right;}
		
		var tmph=(height_bak-margin.top-margin.bottom)/matrix.nodesarr.length;
		if(tmph>25){matrixh=tmph;height=height_bak;}
		else{matrixh=25;height=margin.top+margin.bottom+matrixh*matrix.nodesarr.length;}
		
		svg.attr("width", width).attr("height", height);
		//======================draw nodes===========================
		matrix.nodedom.selectAll("circle").remove();
		var circles=matrix.nodedom.selectAll("circle").data(matrix.nodesarr)
			.enter().append("circle")
			.attr("fill", function(d){
				if (d.type=="uncertain"){return "#c2c2c2";}
				if (d.type=="normal"){return nodecolor_normal(d["certainty"][0]);}
				if (d.type=="abnormal"){return nodecolor_abnormal(d["certainty"][1]);}
			}).attr("stroke","white")
			.attr("stroke-width",function(d){if(d.id==matrix.clickedTlNodeID){return 3;}else{return 1;}})
			.attr("r", noderadius)
			.attr("cx", lefttextw+noderadius).attr("cy", function(d,i){return margin.top+(matrixh-noderadius*2)/2+noderadius+matrixh*i;})
			.on("click",function(d){
				//左击
				console.log(d);
				if(d.id==matrix.clickedTlNodeID){
					Observer.fireEvent("hlSoinnNode",-1,matrix);
					resetHightlight();
				}else{
					Observer.fireEvent("hlSoinnNode",d.id,matrix);
					matrix.clickedTlNodeID=d.id;
					$(".matrix_svg .matrixnodes circle").attr("stroke-width",1);
					$(this).attr("stroke-width",3);
				}
			})
		circles.append("title")
			  .text(function(d) {
				  var tmpcert=_.map(d.certainty, function(num){ return parseFloat(num.toFixed(2)); });
				  return d.id+" threshold:"+d.threshold.toFixed(2)+" wincnt:"+d.wincnt+" "+tmpcert; 
			  });	
		matrix.nodedom_label.selectAll("circle").remove();
		matrix.nodedom_label.selectAll("circle").data(matrix.nodeslabeled)
			.enter().append("circle")
			.attr("fill", "black").attr("r", 3)
			.attr("cx", lefttextw+noderadius)
			.attr("cy", function(d,i){
				var tmparr=_.pluck(matrix.nodesarr,"id");
				return margin.top+(matrixh-noderadius*2)/2+noderadius+matrixh*(_.indexOf(tmparr,d.id));
			});
		
		//==================draw timeslices=======================
		matrix.timedom.selectAll("rect").remove();
		var rects=matrix.timedom.selectAll("rect").data(matrix.timearr)
			.enter().append("rect")
			.attr("fill", function(d,i){
				var tmpcertainty=[0,0,0];
				for(var j=0;j<matrix.nodesarr.length;j++){
					var tmpcert=matrix.certainmatrix[j][i];
					if(tmpcert>0){
						var tmpind=_.indexOf(nodestype,matrix.nodesarr[j]["type"]);
						if(tmpcert>tmpcertainty[tmpind]){tmpcertainty[tmpind]=tmpcert;}
					}
				}
				var tmpmax=_.max(tmpcertainty);
				if (tmpcertainty[2]==tmpmax){return nodecolor_uncertain(tmpcertainty[2]);}
				if (tmpcertainty[0]==tmpmax){return nodecolor_normal(tmpcertainty[0]);}
				if (tmpcertainty[1]==tmpmax){return nodecolor_abnormal(tmpcertainty[1]);}
			}).attr("stroke","white")
			.attr("stroke-width",function(d){if(d==matrix.clickedTlTime){return 3;}else{return 1;}})
			.attr("x", function(d,i){return margin.left+(matrixw-timeslicew)/2+matrixw*i;}).attr("y", toptexth)
			.attr("width", timeslicew).attr("height", timesliceh)
			.on("mousedown",function(d){
				if(d3.event.button==0){
					//左击
					console.log("左击");
					console.log(d);
					if(d==matrix.clickedTlTime){
						Observer.fireEvent("matrixClickTime",-1,matrix);
						resetHightlight();
					}else{
						Observer.fireEvent("matrixClickTime",d*60+Observer.mintime,matrix);
						matrix.clickedTlTime=d;
						$(".matrix_svg .times rect").attr("stroke-width",1);
						$(this).attr("stroke-width",3);
					}
				}else{
					//右击
					console.log("右击");
					matrix.labeledTimeind=d;
					$(".matrix_svg .times rect").attr("stroke-width",1);
					$(this).css("stroke-width",3);
				}
			});
		rects.append("title").text(function(d) {return d*60+Observer.mintime; });	
		
		//==================timeslices right cllick=======================
		$.contextMenu({
            selector: (".matrix_svg .times rect"), 
            callback: function(key, options) {
				if(key=="normal"){
					labeltimeslice("normal",matrix.labeledTimeind);
				}else{
					if(key=="abnormal"){
						labeltimeslice("abnormal",matrix.labeledTimeind);
					}
				}
				resetHightlight();
            },
            items: {
                "normal": {name: "new Normal"},
                "abnormal": {name: "new Abnormal"},
                "cancel": {name: "Cancel"}
            }
        });
		svg.on("mouseup",function(){
			if(event.target.nodeName=="svg"){
				resetHightlight();
				Observer.fireEvent("selectSoinnNode",-1,soinn);
			}
		});
		//==================draw matrix=======================
		matrix.matrixdom.selectAll("g").remove();
		for(var k=0;k<matrix.certainmatrix.length;k++){
			let rects2=matrix.matrixdom.append("g").selectAll("rect")
				.data(matrix.certainmatrix[k])
				.enter().append("rect")
				.attr("fill", function(d,i){
					if(d==0){return "black";}
					var tmptype=matrix.nodesarr[k]["type"];
					if (tmptype=="uncertain"){return nodecolor_uncertain(d);}
					if (tmptype=="normal"){return nodecolor_normal(d);}
					if (tmptype=="abnormal"){return nodecolor_abnormal(d);}
				}).attr("stroke","white")
				.attr("stroke-width",function(d){if(d==matrix.clickedTlTime){return 3;}else{return 1;}})
				.attr("rx",2).attr("ry",2)
				.attr("x", function(d,i){return margin.left+matrixw*i;})
				.attr("y", function(d,i){return margin.top+matrixh*k;})
				.attr("width", matrixw).attr("height", matrixh);
			rects2.append("title").text(function(d) {return d.toFixed(3); });
		}
		
	}
	function labeltimeslice(labeltype,timeind){
		//右击标注时间片
		let obj = {};
		obj.labeledtimeind = JSON.stringify(timeind);
		obj.labeledtype = JSON.stringify(labeltype);
		console.log(obj);
		Observer.fireEvent("updateSoinn_start",[],matrix);
		$.ajax({
			type: 'GET',
			url: 'labelTime',
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				//console.log(evt_data);
				Observer.fireEvent("updateSoinn",[],matrix);
				
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	
	function resetHightlight(){
		//matrix.hightlightNodeID=-1;
		matrix.clickedTlNodeID=-1;
		matrix.clickedTlTime=-1;
		matrix.labeledTimeind=-1;
		$(".matrix_svg .matrixnodes circle").attr("stroke-width",1);
		$(".matrix_svg .times rect").attr("stroke-width",1);
		
	}
	function updatematrix(evt_data){
		matrix.timearr=evt_data.times;
		matrix.certainmatrix=evt_data.matrix;
		matrix.nodesarr=evt_data.nodes;
		matrix.nodeslabeled=[];
		for(var i=0;i<matrix.nodesarr.length;i++){
			if(matrix.nodesarr[i]["labeled"]==1){
				matrix.nodeslabeled.push(matrix.nodesarr[i]);
			}
		}
		drawmatrix();
	}

	function getmatrxidata(obj,url_p){
		$.ajax({
			type: 'GET',
			url: url_p,
			data: obj,
			dataType: 'json',
			success: function(evt_data) {
				console.log(evt_data);
				updatematrix(evt_data);
			},
			error: function(jqXHR) {
				console.log('post error!!', jqXHR);
			},
		});
	}
	function drawdefault(){
		getmatrxidata({"nodeid":JSON.stringify(-1)},'updateMatrix_node');
	}
	drawdefault();
	
    matrix.onMessage = function(message, data, from){
		//console.log(from); 
		if(message=="selectSoinnNode"){
			let obj = {};
			if(data==-1){obj.nodeid = JSON.stringify(-1);matrix.clickedTlNodeID=-1;}
			else{obj.nodeid = JSON.stringify(data[1]);matrix.clickedTlNodeID=data[1];}
			//obj.nodeid = JSON.stringify(20);
			getmatrxidata(obj,'updateMatrix_node');
			
		}
		if(message == "changeTimeRange"){
			let obj = {};
			var tmpind=parseInt((data[1]-60-Observer.mintime)/60);
			console.log(tmpind);
			obj.timeind = JSON.stringify(tmpind);
			matrix.clickedTlTime=tmpind;
			getmatrxidata(obj,'updateMatrix_time');
		}
		if(message == "updateSoinn_end" || message == "re_initmatrix"){
			if(data!=-1){drawdefault();}
		}
		
		
	}
	
	
	Observer.addView(matrix);
	return matrix;
}
	
	
