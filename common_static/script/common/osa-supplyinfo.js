
/**
 * osa-timeset.js
 * date:2012-12-6
 * author:jiangfeng
 */
function boxSupplyInfo(object,id){
	
	var _supplybox_create = function(){
		
		topWindow = $(window.document);
		$(document.body).append("<div id='masklayer'></div>");
		$('#masklayer').css({
			'position':'absolute',
			'left':'0px',
			'top':'0px',
			'width':'100%',
			'min-width':'1024px',
			'height':'100%',
			'background':'#444444',
			'opacity':'0.25',
			'z-index':'9998'
		});
		
		//创建显示ip的弹出层
		topWindow.find('body').append("<div id='window_supply' style='display:none;z-index:9999' class='window_supply'></div>");
		topWindow.find("#window_supply").append("<div class='window_supply_title' id='window_supply_title'></div>");
		topWindow.find("#window_supply").append("<div class='window_supply_con' id='window_supply_con'></div>");
		
		topWindow.find("#window_supply_title").append("<span class='window_supply_text'>补充信息</span><input class='window_supply_close' id='supply_close' type='button'/>");
		
		topWindow.find("#window_supply_con").append("<p><label class='label5'>业务描述：</label><input class='style5' type='text' id='supply_workdes'/></p>");
		topWindow.find("#window_supply_con").append("<p class='light'>可以用一句话介绍该服务器的用途，支撑的业务等,业务描述会作为告警信息的一部分！</p>");
	
		topWindow.find("#window_supply_con").append("<p><label class='label5'>上架时间：</label><input class='style5' type='text' id='supply_time'/></p>");
		topWindow.find("#window_supply_con").append("<p class='light'>上架时间用来记录服务器最初上架的时间，方便管理。</p>");
		topWindow.find("#window_supply_con").append("<p><label class='label5'>设备标签：</label><input class='style5' type='text' id='supply_label' /></p>");
		topWindow.find("#window_supply_con").append("<p class='light'>标签可以用来更好的搜索服务器！</p>");
		topWindow.find("#window_supply_con").append("<p><label class='label5'>设备详情：</label><textarea class='window_supply_textarea' id='supply_info'></textarea></p>");
		topWindow.find("#window_supply_con").append("<p class='light'>可用于记录设备详细情况，比如CPU、内存、采购联系人等。</p>");
		topWindow.find("#window_supply_con").append("<div class='window_supply_line'></div>");		
		topWindow.find("#window_supply_con").append("<div class='right'><input class='updatebut specibut' type='button' id='supply_confirm' value='确定'/><input class='cancelbut specibut' type='button' id='supply_cancel' value='取消'/></div>");
	
		$("#supply_time").datepicker({
			dateFormat: 'yy-mm-dd'
		});
	};
	
	//补充信息弹出层创建
	_supplybox_create();
	
	//补充信心弹出层信息初始化
	var _supplybox_init_value = function(id){
		
		var url = "index.php?c=device&a=device_getvalue";
		$.ajax({
			type:"post",
			url:url,
			dataType:"json",
			data:{'id':id},
			success:function(data){
				$("#supply_workdes").attr('value',data[0].oWorkDes);
				$("#supply_time").attr('value',data[0].oShelveTime);
				$("#supply_label").attr('value',data[0].oDevLabel);
				$("#supply_info").html(data[0].oDevDetail);
			}	
		});
	};
	
	_supplybox_init_value(id);
	
	//时间控件
	$("#supply_time").datepicker({
		dateFormat: 'yy-mm-dd'
	});
	
	
	$("#supply_confirm").click(function(){
		
		var workdes = $("#supply_workdes").val();
		var worktime =$("#supply_time").val();
		var devlabel =$("#supply_label").val();
		var devdetail =$("#supply_info").val();
		if(workdes == worktime == devlabel == devdetail === ''){
			topWindow.find('#window_supply').remove();
			topWindow.find('#masklayer').remove();
		}else{
			var url = "index.php?c=device&a=supply_infos";
			$.post(url,{'id':id,'workdes':workdes,'worktime':worktime,'devlabel':devlabel,'devdetail':devdetail},function(msg){
				topWindow.find('#window_supply').remove();
				topWindow.find('#masklayer').remove();
			});
		}
	});
	
	//事件处理
	$("#supply_close,#supply_cancel").click(function(){
		
		topWindow.find('#window_supply').remove();
		topWindow.find('#masklayer').remove();
	});
	
	var tips_height = topWindow.find('#window_supply').height();
	var tips_width = topWindow.find('#window_supply').width();
	var left = 0;
	var top = 0;
	var scrollTop = $(window.parent.document).scrollTop();
	var screen_height	= $(window).height();
	var screen_width	= $(window).width();
	left = (screen_width - tips_width)/2;
	top = (screen_height - tips_height)/2 + scrollTop;
			
	topWindow.find('#window_supply').css('left',left+'px');
	topWindow.find('#window_supply').css('top',top+'px');
	topWindow.find('#window_supply').css('display','block');

	
	/**************************  draggable  *********************/
	var isMouseDown = false;
	var isMouseMove = false;
	var downX = 0;
	var downY = 0;
	topWindow.find('#window_supply').mousedown(function(e){
		
		isMouseDown = true;
		e=e||evnet;
		downX = parseInt(e.clientX);
		downY = parseInt(e.clientY);
		topWindow.find('body').mousemove(function(e){
			if( !isMouseDown ) return;
			var oleft = parseInt(e.clientX)-downX;
			var otop = parseInt(e.clientY)-downY;
			var left = parseInt( topWindow.find('#window_supply').css('left') ) + oleft;
			var top = parseInt( topWindow.find('#window_supply').css('top') ) + otop;
			
			var screen_height	= $(window.parent).height();
			var screen_width	= $(window.parent).width();
			//计算滚动条偏差
		var sleft = $(window.parent.document).scrollLeft(); 
		var stop = $(window.parent.document).scrollTop(); 
			left = left < 0 ? '0' : left;
			top = top < 0 ? '0' : top;
			left = left >(screen_width + sleft - tips_width) ? screen_width + sleft - tips_width : left;
			top = top >(screen_height + stop - tips_height) ? screen_height + stop - tips_height : top;
			topWindow.find('#window_supply').css('left',left+'px').css('top',top+'px');
			downX = e.clientX;
			downY = e.clientY;
		});
		topWindow.find('body').mouseup(function(e){
			$(this).unbind('mousemove');
			isMouseDown = false;
			downX = 0;
			downY = 0;
		});
	
	});
}
