
/**
 * osa-timeset.js
 * date:2012-12-6
 * author:jiangfeng
 */
function boxShowInfo(object,id){
	
	topWindow = $(window.document);
	var _showbox_create = function(){
		
		topWindow.find('#tanbox').remove();
		//创建显示ip的弹出层
		topWindow.find('body').append("<div id='tanbox' style='display:none;z-index:9999' class='tanbox'></div>");
		topWindow.find("#tanbox").append("<div class='tanbox-con' id='tanbox-con'></div>");
		//初始化
	};
	
	//初始化
	var _showinfo_init = function(){
		
		_showbox_create();	
		var url = "index.php?c=device&a=device_more_message";
		$.post(url,{'id':id},function(msg){
			topWindow.find("#tanbox-con").html('').html(msg);
		});		
	};
	
	_showinfo_init();
	
	var tips_height = topWindow.find('#tanbox').height();
	var tips_width = topWindow.find('#tanbox').width();
	var left = 0;
	var top = 0;
	
	var ttop = object.offset().top;    //TT控件的定位点高  
    var tleft = object.offset().left;    //TT控件的定位点宽   
	left = (tleft - tips_width);
	top = ttop - 120;
			
	topWindow.find('#tanbox').css('left',left+'px');
	topWindow.find('#tanbox').css('top',top+'px');
	topWindow.find('#tanbox').css('display','block');

}
