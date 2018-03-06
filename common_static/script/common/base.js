var winWidth = 0; 
var winHeight = 0; 
function findDimensions() //函数：获取尺寸 
{ 
	//获取窗口宽度 
	if (window.innerWidth) 
	winWidth = window.innerWidth; 
	else if ((document.body) && (document.body.clientWidth)) 
	winWidth = document.body.clientWidth; 

	//通过深入Document内部对body进行检测，获取窗口大小 
	if(document.documentElement && document.documentElement.clientWidth) 
	{ 
		winWidth = document.documentElement.clientWidth; 
	} 
	var isIE = (document.all && window.ActiveXObject && !window.opera) ? true : false;
	if(isIE){
		//结果输出至两个文本框 
		document.getElementById("mainright").style.width= (winWidth-210)+"px"; 
		//document.getElementById("kdd").value= (winWidth-200); 
		if(exist("rightcon_mid")){
			document.getElementById("rightcon_mid").style.width= (winWidth-225)>780?(winWidth-225)+"px":780+"px"; 
		}
	}else{
	//结果输出至两个文本框 
		document.getElementById("mainright").style.width= (winWidth-205)+"px"; 
		//document.getElementById("kdd").value= (winWidth-200); 
		if(exist("rightcon_mid")){
			document.getElementById("rightcon_mid").style.width= (winWidth-220)>780?(winWidth-220)+"px":780+"px"; 
		}
	}
} 
findDimensions(); 
//调用函数，获取数值 
window.onresize=findDimensions; 

function show_ser_option(num){
	var k=num;
	if (k==0){}
	document.getElementById('ser_option').style.display='block';
}

function exist(id){
    var s=document.getElementById(id);
    if(s){return true;}
    else{return false;}
}


$(document).ready(function(){

	setInterval(setAlarmNum,30000);
	
	function setAlarmNum(){
		var url = "index.php?c=home&a=getalarmnum";
		$.post(url,function(msg){
			if(msg == 0){
				$("#alarm-content-notice").hover();
			}else{
				$("#ialarm-content-num").html('').html(msg);
				$("#alarm-content-notice").show();
			}
		});
	}
	

	
	$("#alarm-content-close").click(function(){
		$("#alarm-content-notice").hide();
	});
});
