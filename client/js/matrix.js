
function Matrix(Observer){
	var matrix={};
	
	var $brtDiv=$("#matrix");
    var width=$brtDiv.width();
	var width_bak=width;
    var height=$brtDiv.height();
	var height_bak=height;
	var lefttextw=20;
	var noderadius=6;
	var toptexth=10;
	var timesliceh=15;
	var timeslicew=8;
	var matrixw=17;var matrixh=17;
	var margin = {top: toptexth+timesliceh+9, right: 20, bottom: 20, left: lefttextw+noderadius*2+15};
	
	var svg=d3.select("#matrix")
			.append("svg")
			.attr("width", width)
			.attr("height", height).attr("class","matrix_svg");
	
	var $brtDiv2=$("#matrix_hist");
    var width2=$brtDiv2.width();
    var height2=$brtDiv2.height();
	var svg2=d3.select("#matrix_hist")
			.append("svg")
			.attr("width", width2)
			.attr("height", height2);
	
	matrix.nodedom = svg.append("g").attr("class", "matrixnodes");
	matrix.nodedom_label = svg.append("g").attr("class", "nodes_labeled");
	matrix.timedom = svg.append("g").attr("class", "times");
	matrix.timehistdom = svg2.append("g").attr("class", "timehist");
	matrix.timehisthldom = svg2.append("g").attr("class", "timehisthl");
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
		//var tmph=(height_bak-margin.top-margin.bottom)/matrix.nodesarr.length;
		//if(tmph>17){matrixh=tmph;height=height_bak;}
		//else{tmph=17;matrixh=17;height=margin.top+margin.bottom+matrixh*matrix.nodesarr.length;}
		//matrixw=tmph;
		width=margin.left+matrixw*matrix.timearr.length+margin.right;
		
		svg.attr("width", width).attr("height", height);
		/*
		var timehish=height-margin.top-matrixh*matrix.nodesarr.length;
		if(timehish>30){timehish=30;}
		var x_scale = d3.scaleTime().range([margin.left,margin.left+matrixw*matrix.timearr.length])
			.domain([new Date(Observer.mintime*1000-8*60*60*1000),new Date((Observer.starttime)*1000-8*60*60*1000)]);
		var histw=x_scale(new Date((Observer.mintime+60)*1000))-x_scale(new Date(Observer.mintime*1000));
		if(histw<1){histw=1;}
		*/
		var timehish=height2-20-5;
		var x_scale = d3.scaleTime().range([margin.left,width2-margin.right])
			.domain([new Date(Observer.mintime*1000-8*60*60*1000),new Date((Observer.starttime)*1000-8*60*60*1000)]);
		var histw=x_scale(new Date((Observer.mintime+60)*1000))-x_scale(new Date(Observer.mintime*1000));
		if(histw<1){histw=1;}
		//======================draw nodes===========================
		matrix.nodedom.selectAll("circle").remove();
		var circles=matrix.nodedom.selectAll("circle").data(matrix.nodesarr)
			.enter().append("circle")
			.attr("fill", function(d){
				//if (d.type=="uncertain"){return "#c2c2c2";}
				//if (d.type=="normal"){return nodecolor_normal(d["certainty"][0]);}
				//if (d.type=="abnormal"){return nodecolor_abnormal(d["certainty"][1]);}
				if(d["certainty"][2]==1){return "#c2c2c2";}
				if (d.type=="normal" || (d["certainty"][0]>d["certainty"][1])){return nodecolor_normal(d["certainty"][0]);}
				if (d.type=="abnormal" || (d["certainty"][1]>d["certainty"][0])){return nodecolor_abnormal(d["certainty"][1]);}
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
			})
			.on("mouseover",function(d,i){
				matrix.timehisthldom.append("rect")
					.attr("fill", "pink")
					.attr("x", function(){
						return x_scale(new Date((d*60+Observer.mintime)*1000-8*60*60*1000));
					})
					.attr("y", 5)
					.attr("width", histw*3).attr("height", timehish)
			}).on("mouseout",function(){
				//console.log("k");
				matrix.timehisthldom.selectAll("rect").remove();
			});
		rects.append("title").text(function(d) {
			var daydiffer=Math.floor((d*60)/(24*3600))
			var curTime=d*60+Observer.mintime; 
			var tmpDate=new Date(curTime*1000-8*60*60*1000);
			var dayselected=daydiffer;
			var hourselected=tmpDate.getHours();
			var minuteselected=tmpDate.getMinutes();
			return "4."+(dayselected+1)+" "+hourselected+":"+minuteselected; 
		});	
		
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
		//==================draw time histogram=======================
		
		matrix.timehistdom.selectAll("g").remove();
		matrix.timehistdom.append("g").selectAll("rect").data(matrix.timearr)
			.enter().append("rect")
			.attr("fill", "white")
			.attr("x", function(d,i){return x_scale(new Date((d*60+Observer.mintime)*1000-8*60*60*1000));})
			.attr("y", 5)
			.attr("width", histw).attr("height", timehish)
		matrix.timehistdom.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + (height2-20) + ")")
			.call(d3.axisBottom(x_scale));
		
		//==================draw matrix=======================
		matrix.matrixdom.selectAll("g").remove();
		for(var k=0;k<matrix.certainmatrix.length;k++){
			let rects2=matrix.matrixdom.append("g").selectAll("rect")
				.data(matrix.certainmatrix[k])
				.enter().append("rect")
				.attr("fill", function(d,i){
					if(d==0){return "black";}
					var tmptype=matrix.nodesarr[k]["type"];
					var tmpcertainty=matrix.nodesarr[k]["certainty"];
					//if (tmptype=="uncertain"){return nodecolor_uncertain(d);}
					//if (tmptype=="normal"){return nodecolor_normal(d);}
					//if (tmptype=="abnormal"){return nodecolor_abnormal(d);}
					if(tmpcertainty[2]==1){return "#c2c2c2";}
					if (tmptype=="normal" || (tmpcertainty[0]>tmpcertainty[1])){return nodecolor_normal(d);}
					if (tmptype=="abnormal" || (tmpcertainty[1]>tmpcertainty[0])){return nodecolor_abnormal(d);}
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
	
	
