/***********************************select 特效事件重写 ************************************************/
	$(".tag_input").live("click",function(){
		//当前select伸缩
		var tagObject = $(this);
		$(".tag_input").not(this).each(function(){
			ul_hide($(this).parent());
		});
		if(tagObject.is('.tag_select')){
			ul_show(tagObject.parent());
		}else if(tagObject.is('.tag_hover')){
			ul_hide(tagObject.parent());
		}	
	});
	
	$(".tag_li").live("click",function(){
		var liObject = $(this);
		var value = liObject.html();
		var selObject = liObject.parent().children('.open_selected');
		selObject.removeClass('open_selected');
		selObject.addClass('open');
		
		liObject.removeClass('open');
		liObject.addClass('open_selected');
		ul_hide(liObject.parent().parent());
		liObject.parent().parent().find('input').attr('value',value);
	});
	
	function ul_show(object){	
		var inputObject = object.find('input');
		var ulObject = object.find('ul');
		inputObject.removeClass('tag_select');
		inputObject.addClass('tag_hover');
		ulObject.show();
		object.css({'z-index':'10'});
	}
	
	function ul_hide(object){
		var inputObject = object.find('input');
		var ulObject = object.find('ul');
		inputObject.addClass('tag_select');
		inputObject.removeClass('tag_hover');
		ulObject.hide();
		object.css({'z-index':'1'});	
	}
	
	function ul_hide_all(){		
		$('.tag_input').addClass('tag_select');
		$('.tag_input').removeClass('tag_hover');
		$('.tag_options').hide();
		$('.select_box').css({'z-index':'1'});
	}
	
	$("input[name!='tag_input']").click(function(){
		ul_hide_all();
	});