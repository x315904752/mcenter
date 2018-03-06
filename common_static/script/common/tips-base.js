/**
 * tip-base.js
 * date:2012-9-21
 * author:jiangfeng
 */
function tipsConfirm(msg,callback){
	
	//创建遮罩
	topWindow = $(window.document);
	//topWindow.find('head').append(css);
	$(document.body).append("<div id='coverlayer'></div>");
	$('#coverlayer').css({
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
	
	//tips 主体
	topWindow.find('body').append("<div id='tips-window' style='display:none;z-index:9999' class='tips-window'></div>");
	topWindow.find('#tips-window').append("<div id='tips-window-title' class='tips-window-title'></div>");
	topWindow.find('#tips-window-title').append("<span class='tips-text'>系统提示</span>");
	topWindow.find('#tips-window-title').append("<input id='tips-close' class='tips-close' type='button' >");
	topWindow.find('#tips-window').append("<div id='tips-window-content' class='tips-window-content'></div>");
	topWindow.find('#tips-window-content').append("<label class='tips-label-img'></label>");
	topWindow.find('#tips-window-content').append("<label class='tips-label-msg'>"+msg+"</label>");
	topWindow.find('#tips-window-content').append("<div class='tips-clear'></div>");
	topWindow.find('#tips-window-content').append("<div id='tips-right' class='tips-right'></div>");
	topWindow.find('#tips-right').append("<input id='tips-btn-true' type='button' class='tips-btn' value='确定'>");
	topWindow.find('#tips-right').append("<input id='tips-btn-false' type='button' class='tips-btn' value='取消'>");
	
	
	topWindow.find('#tips-btn-true').focus();
	//事件处理
	
	topWindow.keyup(function(event){
		if( event.keyCode == 9 ){//'Tab' is not allowed
			topWindow.find('#tips-btn-true').focus();
			return false;
		}
		if( event.keyCode == 27 ){
			topWindow.find('#tips-window').remove();
			topWindow.find('#coverlayer').remove();
			if(callback){
				callback(false);
			}
			return false;
		}
	});
	topWindow.find("#tips-btn-true").click(function(){
		topWindow.find('#tips-window').remove();
		topWindow.find('#coverlayer').remove();
		if(callback){
			callback(true);
		}
		return true;
	});
	topWindow.find("#tips-btn-false").click(function(){
		topWindow.find('#tips-window').remove();
		topWindow.find('#coverlayer').remove();
		if(callback){
			callback(false);
		}
		return false;
	});
	
	topWindow.find("#tips-close").click(function(){
		topWindow.find('#tips-window').remove();
		topWindow.find('#coverlayer').remove();
		if(callback){
			callback(false);
		}
		return false;
	});
	
	//计算position
	var tips_height = topWindow.find('#tips-window').height();
	var tips_width = topWindow.find('#tips-window').width();
	var left = 0;
	var top = 0;
	var scrollTop = $(window.parent.document).scrollTop();
	var screen_height	= $(window).height();
	var screen_width	= $(window).width();
	left = (screen_width - tips_width)/2;
	top = (screen_height - tips_height)/2+scrollTop;
	
	
	topWindow.find('#tips-window').css('left',left+'px');
	topWindow.find('#tips-window').css('top',top+'px');
	topWindow.find('#tips-window').css('display','block');
	
	topWindow.find('#tips-btn-true').focus();
	
	
	/**************************  draggable  *********************/
	var isMouseDown = false;
	var isMouseMove = false;
	var downX = 0;
	var downY = 0;
	topWindow.find('#tips-window').mousedown(function(e){
		
		isMouseDown = true;
		e=e||evnet;
		downX = parseInt(e.clientX);
		downY = parseInt(e.clientY);
		topWindow.find('body').mousemove(function(e){
			if( !isMouseDown ) return;
			var oleft = parseInt(e.clientX)-downX;
			var otop = parseInt(e.clientY)-downY;
			var left = parseInt( topWindow.find('#tips-window').css('left') ) + oleft;
			var top = parseInt( topWindow.find('#tips-window').css('top') ) + otop;
			
			var screen_height	= $(window.parent).height();
			var screen_width	= $(window.parent).width();
			//计算滚动条偏差
		var sleft = $(window.parent.document).scrollLeft(); 
		var stop = $(window.parent.document).scrollTop(); 
			left = left < 0 ? '0' : left;
			top = top < 0 ? '0' : top;
			left = left >(screen_width + sleft - tips_width) ? screen_width + sleft - tips_width : left;
			top = top >(screen_height + stop - tips_height) ? screen_height + stop - tips_height : top;
			topWindow.find('#tips-window').css('left',left+'px').css('top',top+'px');
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


function tipsAlert(msg,callback){
	
	//创建遮罩
	topWindow = $(window.document);
	$(document.body).append("<div id='coverlayer'></div>");
	$('#coverlayer').css({
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
	
	//tips 主体
	topWindow.find('body').append("<div id='tips-window' style='display:none;z-index:19999;position:absolute;' class='tips-window'></div>");
	topWindow.find('#tips-window').append("<div id='tips-window-title' class='tips-window-title'></div>");
	topWindow.find('#tips-window-title').append("<span class='tips-text'>系统提示</span>");
	topWindow.find('#tips-window-title').append("<input id='tips-close' class='tips-close' type='button' >");
	topWindow.find('#tips-window').append("<div id='tips-window-content' class='tips-window-content'></div>");
	topWindow.find('#tips-window-content').append("<label class='tips-label-img'></label>");
	topWindow.find('#tips-window-content').append("<label class='tips-label-msg'>"+msg+"</label>");
	topWindow.find('#tips-window-content').append("<div class='tips-clear'></div>");
	topWindow.find('#tips-window-content').append("<div id='tips-right' class='tips-right'></div>");
	topWindow.find('#tips-right').append("<input id='tips-btn-true' type='button' class='tips-btn' value='确定'>");
	//topWindow.find('#tips-right').append("<input id='tips-btn-false' type='button' class='tips-btn' value='取消'>");
	
	
	topWindow.find('#tips-btn-true').focus();
	//事件处理
	
	topWindow.keyup(function(event){
		if( event.keyCode == 9 ){//'Tab' is not allowed
			topWindow.find('#tips-btn-true').focus();
			return false;
		}
		if( event.keyCode == 27 ){
			topWindow.find('#tips-window').remove();
			topWindow.find('#coverlayer').remove();
			if(callback){
				callback(true);
			}
			return false;
		}
	});
	topWindow.find("#tips-btn-true").click(function(){
		topWindow.find('#tips-window').remove();
		topWindow.find('#coverlayer').remove();
		if(callback){
			callback(true);
		}
		return true;
	});

	
	topWindow.find("#tips-close").click(function(){
		topWindow.find('#tips-window').remove();
		topWindow.find('#coverlayer').remove();
		if(callback){
			callback(false);
		}
		return false;
	});
	
	//计算position
	var tips_height = topWindow.find('#tips-window').height();
	var tips_width = topWindow.find('#tips-window').width();
	var left = 0;
	var top = 0;
	var scrollTop = $(window.parent.document).scrollTop();
	var screen_height	= $(window).height();
	var screen_width	= $(window).width();
	left = (screen_width - tips_width)/2;
	top = (screen_height - tips_height)/2+scrollTop;
	
	
	topWindow.find('#tips-window').css('left',left+'px');
	topWindow.find('#tips-window').css('top',top+'px');
	topWindow.find('#tips-window').css('display','block');
	
	topWindow.find('#tips-btn-true').focus();
	
	/**************************  draggable  *********************/
	var isMouseDown = false;
	var isMouseMove = false;
	var downX = 0;
	var downY = 0;
	topWindow.find('#tips-window').mousedown(function(e){
		
		isMouseDown = true;
		e=e||evnet;
		downX = parseInt(e.clientX);
		downY = parseInt(e.clientY);
		topWindow.find('body').mousemove(function(e){
			if( !isMouseDown ) return;
			var oleft = parseInt(e.clientX)-downX;
			var otop = parseInt(e.clientY)-downY;
			var left = parseInt( topWindow.find('#tips-window').css('left') ) + oleft;
			var top = parseInt( topWindow.find('#tips-window').css('top') ) + otop;
			
			var screen_height	= $(window.parent).height();
			var screen_width	= $(window.parent).width();
			//计算滚动条偏差
		var sleft = $(window.parent.document).scrollLeft(); 
		var stop = $(window.parent.document).scrollTop(); 
			left = left < 0 ? '0' : left;
			top = top < 0 ? '0' : top;
			left = left >(screen_width + sleft - tips_width) ? screen_width + sleft - tips_width : left;
			top = top >(screen_height + stop - tips_height) ? screen_height + stop - tips_height : top;
			topWindow.find('#tips-window').css('left',left+'px').css('top',top+'px');
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

function devicePop(){
	//创建遮罩
	topWindow = $(window.document);
	$(document.body).append("<div id='coverlayer'></div>");
	$('#coverlayer').css({
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
	
	//	
	topWindow.find('#device-pop').css({'display':'none','z-index':9999,'position':'absolute'});
	
	//事件处理
	topWindow.find("#close-pop").click(function(){
		topWindow.find('#device-pop').css({'display':'none','z-index':-1});
		topWindow.find('#coverlayer').remove();
		return false;
	});
	
	topWindow.find("#cancel-pop").click(function(){
		topWindow.find('#device-pop').css({'display':'none','z-index':-1});
		topWindow.find('#coverlayer').remove();
		return false;
	});
	
	/************************************ input 验证 ***************************************************/
	$.ajaxSetup({
		  async: false
	}); 
	var flag = true ;
	/*********devname验证********/
	$('#devname-pop').click(function(){
		$("#devname-tips").html('');	
	});
	$('#devname-pop').blur(function(){
		var devname = $.trim($(this).val());
		if(devname == ''){
			$("#devname-tips").css({'color':'rgb(263,24,13)'}).html('请输入正确格式的设备名');
			flag = false;
			//return;
		}else if(devname!=devname.match(/^[a-zA-Z0-9\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.\_\@]+$/)){
			$("#devname-tips").css({'color':'rgb(263,24,13)'}).html('请输入正确格式的设备名');
			flag = false;
			//return ;
		}else{
			$("#devname-tips").html('');	
		}
	});
	
	/******ipname验证*******/
	$('#ipname-pop').click(function(){
		$("#ip-tips").css({'color':'rgb(23,124,226)'}).html('');
	});
	
	function isip(ip){		
		var re=/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;//正则表达式   
		if(re.test(ip))   
		{   
			if( RegExp.$1<256 && RegExp.$2<256 && RegExp.$3<256 && RegExp.$4<256) 
			return true;   
		}
		return false ;
	}
	$('#ipname-pop').blur(function(){
		var ip = $.trim($(this).val());
		var url = 'index.php?c=device&a=ip_check';
		if(ip == ''){
			$("#ip-tips").css({'color':'rgb(263,24,13)'}).html('请输入正确格式的ip');
			flag = false;
			//return;
		}else if(!isip(ip)){
			$("#ip-tips").css({'color':'rgb(263,24,13)'}).html('请输入正确格式的ip');
			flag = false;
			//return ;
		}else{
			$.post(url,{'ip':ip},function(msg){
				if(msg.indexOf('success')!=-1){
					$("#ip-tips").css({'color':'rgb(23,124,226)'}).html('');
				}else if(msg.indexOf('exists')!=-1){
					$("#ip-tips").css({'color':'rgb(263,24,13)'}).html('该ip已经存在');
					flag = false;
				}		
			});	
		}
	});
	
	//确定按钮
	$("#confirm-pop").click(function(){
		flag = true ;
		$('#devname-pop').blur();
		$('#ipname-pop').blur();
		if(flag == false){
			return false;
		}
		var devname = $.trim($('#devname-pop').val());
		var ipname = $.trim($("#ipname-pop").val());
		var devtype = $.trim($("#device-pop").find(".tag_input").val());
		if(devtype == '请选择类型'){
			devtype = '';
		}
		var url = 'index.php?c=device&a=pop_device_add';
		$.post(url,{
			'devname':devname,
			'ipname':ipname,
			'devtype':devtype
		},function(msg){
			topWindow.find('#device-pop').css({'display':'none','z-index':-1});
			topWindow.find('#coverlayer').remove();
			type_deal(devtype);
			tipsAlert('设备添加成功！');
			topWindow.find('.Illustrations').children(":first").before(msg);
			//window.location = 'index.php?c=device&a=graphindex';		
		});
		
	});
	
	/*********  新增设备类型 select 处理************/
	function li_addtype(devtype){
		//先全局后局部
		var content = "<li class='open tag_li'>"+devtype+"</li>";
		$("#device-pop").find('ul').append(content);		
	}
	
	function type_check(devtype){
		if(devtype == ''){
			return true;
		}
		for(i in typeArr){
			if($.trim(typeArr[i])==$.trim(devtype)){
				return true;
			}
		}
		return false;
	}
	
	function type_deal(devtype){
		if(type_check(devtype)==false){
			li_addtype(devtype);
			typeArr.push(devtype);
		}
	}
	
	
	//计算position 
	var tips_height = topWindow.find('#device-pop').height();
	var tips_width = topWindow.find('#device-pop').width();
	var left = 0;
	var top = 0;
	var scrollTop = $(window.parent.document).scrollTop();
	var screen_height	= $(window).height();
	var screen_width	= $(window).width();
	left = (screen_width - tips_width)/2;
	top = (screen_height - tips_height)/2+scrollTop;
	
	topWindow.find('#device-pop').css('left',left+'px');
	topWindow.find('#device-pop').css('top',top+'px');
	topWindow.find('#device-pop').css('display','block');
}


function osaUpload(){
	
	
}