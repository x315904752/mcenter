$(document).ready(function(){
	
	/**************************************list 的页面特效控制*********************************/
	$("#more_select,").click(function(){
		$("#morecond_div").toggle("slow");	
	});
	
	$("#key_2").blur(function(){
		$("#key_2_open").hide();	
	});
	$("#key_2").click(function(){
		$("#key_2_open").show();
		$("#key_2").attr('value','');
		$("#key_2").removeClass('input1').addClass('input2');
	});
	
	$(".search_li").click(function(){
		var value = $.trim($(this).html());
		$("#key_2").attr('value',value);
		$("#key_2_open").hide();
	});
	
	/***********************************list record 页面处理************************************/
	$(".show-li").live("click",function(){
		$(this).parent().hide();
		var editObject = $(this).parent().parent().find(".list-edit");
		editObject.show();
		if(editObject.find('.rd_server').find('input').val() == ''){
			editObject.find('.rd_server').find('ul').children(":first").removeClass('open');
			editObject.find('.rd_server').find('ul').children(":first").addClass('open_selected');
			editObject.find('.rd_server').find('input').attr('value','请选择或输入类型');
		}
		if(editObject.find('.rdplace').find('input').val() == ''){
			editObject.find('.rdplace').find('ul').children(":first").removeClass('open');
			editObject.find('.rdplace').find('ul').children(":first").addClass('open_selected');
			editObject.find('.rdplace').find('input').attr('value','请选择或输入机房');	
		}
		ul_hide_all();
	});
	
	$("#record-add").click(function(){
		$(".list-clone:hidden").clone(true).removeClass("none").prependTo("#rightcon_mid");
		ul_hide_all();
	});
	
	
	$(".list-edit-exit").live("click",function(){
		ul_hide_all();
		var parent = $(this).parent().parent().parent();		//alert(parent);
		//parent.hide();
		parent.children('.list-edit').hide();
		parent.children('.list-li').show();
		//ul_hide_all();
	});
	
	$(".list-add-exit").live("click",function(){
		ul_hide_all();
		$(this).parent().parent().parent().remove();
	});
	

	
	/************************************** list 编辑与添加 **********************************************/
	
	$.ajaxSetup({
		  async: false
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
	
	function tips_show(type,object,msg){
		if(type =='devtype'){
			var ttop = object.find('.rdname').offset().top;
			var tleft = object.find('.rdname').offset().left;
			$("#actprompt").css({position:'absolute',top:ttop-50,left:tleft+50});	
		}else if(type='ip'){
			var ttop = object.find('.rdip').offset().top;
			var tleft = object.find('.rdip').offset().left;
			$("#actprompt").css({position:'absolute',top:ttop-50,left:tleft-30});
		}	
		$("#actprompt").find('.data').html(msg);
		$("#actprompt").show();
	}
	
	$(".list-add-save").live("click",function(){
		var saveObject = $(this).parent().parent();
		var devname = $.trim(saveObject.find('.rdname').find('input').val());
		if(devname == ''){
			var msg='设备名称不能为空';
			tips_show('devtype',saveObject,msg);
			return false;
		}else if(devname!=devname.match(/^[a-zA-Z0-9\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.\_\@]+$/)){
			var msg='设备名称不合法';
			tips_show('devtype',saveObject,msg);
			return false;
		}else{
			$("#actprompt").hide();
		}
		var ipname = $.trim(saveObject.find('.rdip').find('input').val());
		if(ipname == ''){
			var msg = 'ip不能为空';
			tips_show('ip',saveObject,msg);
			return false;
			
		}else if(!isip(ipname)){
			var msg = 'ip不合法';
			tips_show('ip',saveObject,msg);
			return false;		
		}else{
			var url = 'index.php?c=device&a=ip_check';
			var flag = true;
			$.post(url,{'ip':ipname},function(msg){
				if(msg.indexOf('success')!=-1){
					$("#actprompt").hide();
				}else if(msg.indexOf('exists')!=-1){
					var msg = 'ip不唯一';
					tips_show('ip',saveObject,msg);
					flag = false;
				}		
			});
			if(flag == false){
				return false;
			}
		}
		var devtype = $.trim(saveObject.find('.rd_server').find('input').val());
		if(devtype == '请选择或输入类型'){
			devtype = '';
		}

		var engineroom = $.trim(saveObject.find('.rdplace').find('input').val());
		if(engineroom == '请选择或输入机房'){
			engineroom = '';
		}
		var devprice = $.trim(saveObject.find('.rdbuy').find('input').val());
		var tgprice = $.trim(saveObject.find('.rddeposit').find('input').val());
		var targetUrl = 'index.php?c=device&a=list_add_ajax';
		$.post(targetUrl,{
			'devname':devname,
			'ipname':ipname,
			'devtype':devtype,
			'engineroom':engineroom,
			'devprice':devprice,
			'tgprice':tgprice
		},function(msg){
			saveObject.before(msg);
			edit_transform(saveObject);
			input_replace(saveObject,ipname);
			type_deal(saveObject.find('.rd_server'),devtype);
			room_deal(saveObject.find('.rdplace'),engineroom);
		});
	});
	
	
	//编辑
	$(".list-edit-save").live("click",function(){
		var saveObject = $(this).parent().parent();
		var id = saveObject.parent().find('.select_all').attr('value');
		var devname = $.trim(saveObject.find('.rdname').find('input').val());
		if(devname == ''){
			var msg='设备名称不能为空';
			tips_show('devtype',saveObject,msg);
			return false;
		}else if(devname!=devname.match(/^[a-zA-Z0-9\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5\.\_\@]+$/)){
			var msg='设备名称不合法';
			tips_show('devtype',saveObject,msg);
			return false;
		}else{
			$("#actprompt").hide();
		}
		var ipname = $.trim(saveObject.find('.rdip').find('input').val());
		var devtype = $.trim(saveObject.find('.rd_server').find('input').val());
		var ipid = $.trim(saveObject.parent().find('.select_hide').val());
		if(devtype == '请选择或输入类型'){
			devtype = '';
		}

		var engineroom = $.trim(saveObject.find('.rdplace').find('input').val());
		if(engineroom == '请选择或输入机房'){
			engineroom = '';
		}
		var devprice = $.trim(saveObject.find('.rdbuy').find('input').val());
		var tgprice = $.trim(saveObject.find('.rddeposit').find('input').val());
		var targetUrl = 'index.php?c=device&a=list_edit_ajax';
		$.post(targetUrl,{
			'id':id,
			'devname':devname,
			'ipname':ipname,
			'ipid':ipid,
			'devtype':devtype,
			'engineroom':engineroom,
			'devprice':devprice,
			'tgprice':tgprice
		},function(msg){
			saveObject.parent().find('.list-li').find('.show-li').remove();
			saveObject.parent().find('.list-li').find('.rdaction').before(msg);
			edit_transform(saveObject);
			type_deal(saveObject.find('.rd_server'),devtype);
			room_deal(saveObject.find('.rdplace'),engineroom);
		});
	});
	
	
	/**************************************** 添加,编辑 关联事件处理**********************************/
	function edit_transform(object){
		object.find('.rdaction').find('.actsave').removeClass('list-add-save');
		object.find('.rdaction').find('.actsave').addClass('list-edit-save');
		object.find('.rdaction').find('.actexit').removeClass('list-add-exit');
		object.find('.rdaction').find('.actexit').addClass('list-edit-exit');
		object.hide();
		object.parent().children('.list-li').show();		
	}
	
	function input_replace(object,ip){
		inputObject = object.find('.rdip').find('input');
		inputObject.before("<input value="+ip+" readonly='readonly'>");
		inputObject.remove();
	}
	
	function li_addtype(object,devtype){
		//先全局后局部
		var content = "<li class='open tag_li'>"+devtype+"</li>";
		$(".rd_server").find('ul').append(content);
		object.find('ul').find('.open_selected').addClass('open');
		object.find('ul').find('.open_selected').removeClass('open_selected');
		object.find('ul').children(':last').addClass('open_selected');
		object.find('ul').children(':last').removeClass('open');		
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
	
	function type_deal(object,devtype){
		if(type_check(devtype)==false){
			li_addtype(object,devtype);
			typeArr.push(devtype);
		}
	}
	
	function room_deal(object,engineroom){
		if(room_check(engineroom)==false){
			li_addroom(object,engineroom);
			roomArr.push(engineroom);
		}		
	}
	
	function room_check(engineroom){
		if(engineroom == ''){
			return true;
		}
		for(i in roomArr){
			if($.trim(roomArr[i])==$.trim(engineroom)){
				return true;
			}
		}
		return false;
	}
	
	function li_addroom(object,engineroom){
		//先全局后局部
		var content = "<li class='open tag_li'>"+engineroom+"</li>";
		$(".rdplace").find('ul').append(content);
		object.find('ul').find('.open_selected').addClass('open');
		object.find('ul').find('.open_selected').removeClass('open_selected');
		object.find('ul').children(':last').addClass('open_selected');
		object.find('ul').children(':last').removeClass('open');		
	}
	
	/************************************暂停，启用，删除等操作***********************************************/
	
	$(".list-pause").live("click",function(){
		var object = $(this);
		var id = $(this).parent().parent().parent().find('.select_all').attr('value');
		var ipid = $(this).parent().parent().parent().find('.select_hide').val();
		var url = "index.php?c=device&a=device_stop";
		$.post(url,{'id':id,'ipid':ipid},function(msg){
			object.hide();
			object.parent().find('.list-open').show();
		});	

	});
	
	$(".list-open").live("click",function(){
		var object = $(this);
		var id = $(this).parent().parent().parent().find('.select_all').attr('value');
		var ipid = $(this).parent().parent().parent().find('.select_hide').val();
		var url = "index.php?c=device&a=device_open";
		$.post(url,{'id':id,'ipid':ipid},function(msg){
			object.hide();
			object.parent().find('.list-pause').show();
		});	
	});
	
	$(".list-del").live("click",function(){
		var object = $(this);
		var id = $(this).parent().parent().parent().find('.select_all').attr('value');
		var ipid = $(this).parent().parent().parent().find('.select_hide').val();
		var url = "index.php?c=device&a=device_del";
		var callback = function(result){
			if(result==true){
				$.post(url,{'id':id,'ipid':ipid},function(msg){
					object.parents('.list-unit').remove();
				});	
			}
		};
		var msg = '删除后记录不可恢复，确认删除吗？';
		tipsConfirm(msg,callback);
	});
	
	/******************************批量删除,暂停,启用***************************************/
	
	function record_tranform(type){
		$(".select_all:visible").each(function(){
			if(type == 'pause'){
				if($(this).is(":checked")){
					object = $(this).parent().parent();
					object.find('.list-open').show();
					object.find('.list-pause').hide();
				}
			}else if(type=='open'){
				if($(this).is(":checked")){
					object = $(this).parent().parent();
					object.find('.list-pause').show();
					object.find('.list-open').hide();
				}
			}
			else if(type=='del'){
				if($(this).is(":checked")){
					object = $(this).parent().parent().parent();
					object.remove();
				}	
			}
		});	
		$(":checkbox").attr('checked',false);
	}
	
	//批量暂停
	$("#record-pause").click(function(){
		var idarr = new Array();
		var iparr = new Array();
		$(".select_all:visible").each(function(){
			if($(this).is(":checked")){
				idarr.push($(this).attr('value'));
				iparr.push($(this).parent().find('.select_hide').val());
			}
		});
		if(idarr.length == 0){
			var msg = '请选择需要暂停的项';
			tipsAlert(msg);
			return false;
		}
		var url = "index.php?c=device&a=device_stop_batch";
		$.post(url,{'idarr':idarr,'iparr':iparr},function(msg){
			record_tranform('pause');
		});
	});
	
	//批量开启
	$("#record-open").click(function(){
		var idarr = new Array();
		var iparr = new Array();
		$(".select_all:visible").each(function(){
			if($(this).is(":checked")){
				idarr.push($(this).attr('value'));
				iparr.push($(this).parent().find('.select_hide').val());
			}
		});
		if(idarr.length == 0){
			var msg = '请选择需要启用的项';
			tipsAlert(msg);
			return false;
		}
		var url = "index.php?c=device&a=device_open_batch";
		$.post(url,{'idarr':idarr,'iparr':iparr},function(msg){
			record_tranform('open');
		});
	});
	
	//批量删除
	$("#record-del").click(function(){
		var idarr = new Array();
		var iparr = new Array();
		$(".select_all:visible").each(function(){
			if($(this).is(":checked")){
				idarr.push($(this).attr('value'));
				iparr.push($(this).parent().find('.select_hide').val());
			}
		});
		if(idarr.length == 0){
			var msg = '请选择需要删除的项';
			tipsAlert(msg);
			return false;
		}
		var callback = function(result){
			if(result == true){
				var url = "index.php?c=device&a=device_del_batch";
				$.post(url,{'idarr':idarr,'iparr':iparr},function(msg){
					record_tranform('del');
				});
			}
		};
		var msg ='删除后记录不可恢复，确认删除吗？';
		tipsConfirm(msg,callback);
	});
	
	//全选
	$("#check_all").click(function(){
		$(".sel_all_input").attr('checked',this.checked);
	});
	
	$("input").click(function(){
		$("#actprompt").hide();
	});
	
	
	/***********************************ajax 搜索处理**************************************************/
	function records_ajaxshow(info){
		$('.list-unit').hide();
		info = eval(info);
		for(i in info){
			$('.select_all').each(function(){
				var checkid = $(this).attr('value');
				if(checkid == info[i].id){
					$(this).parent().parent().parent().show();
				}
			});
		}	
	}
	
	$("#record_search").keyup(function(){
		var url = "index.php?c=device&a=list_search";
		var value = $.trim($(this).val());
		$.post(url,{'search':value},function(info){
			records_ajaxshow(info);	
		});
	});
	
	
	/*********隐藏 高级搜索事件处理**********/
	$(".type-select").click(function(){
		var tyname = $(this).html();
		$(".type-selected").html(tyname);
		var lname = $(".label-selected").html();
		if(tyname == "全部类型"){
			tyname = '';
		}
		if(lname == "所有标签"){	
			lname = '';
		}
		var url = 'index.php?c=device&a=list_retrieve';
		$.post(url,{'typename':tyname,'labelname':lname},function(info){
			records_ajaxshow(info);
		});
	});
	
	$(".label-select").click(function(){
		var lname = $(this).html();
		$(".label-selected").html(lname);
		var tyname = $(".type-selected").html();
		if(tyname == "全部类型"){
			tyname = '';
		}
		if(lname == "所有标签"){	
			lname = '';
		}
		var url = 'index.php?c=device&a=list_retrieve';
		$.post(url,{'typename':tyname,'labelname':lname},function(info){
			records_ajaxshow(info);	
		});
	});
	
	$(".clear-select").click(function(){
		$(".type-selected").html("全部类型");
		$(".label-selected").html("所有标签");
		var url = 'index.php?c=device&a=list_retrieve';
		$.post(url,{'typename':'','labelname':''},function(info){
			records_ajaxshow(info);	
		});
		$("#morecond_div").hide();
	});
	
	$(".actprompt0").mouseover(function(){
		var id = $(this).parents('.record-list').find('.select_all').attr('value');
		var object = $(this);
		boxShowInfo(object,id);
	}).mouseout(function(){
		$(window.document).find("#tanbox").remove();
	});
	
	
	$(".list-msg").click(function(){
		
		var object = $(this);
		var id = $(this).parents(".record-list").find(".select_all").attr('value');
		boxSupplyInfo(object,id);
	});
	
	
	
	
});
