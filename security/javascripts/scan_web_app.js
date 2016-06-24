var RTCPeerConnection = window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
function ipCreate(ip){
	var ips = ip.replace(/(\d+\.\d+\.\d+)\.\d+/,'$1.');
	for(var i=1;i<=255;i++){
		ElementCreate(ips+i,"80","apache_pb.gif");
		ElementCreate(ips+i,"8087","apache_pb.gif");
		ElementCreate(ips+i,"8080","apache_pb.gif");//添加要扫描的端口
	}
}
function ElementCreate(ip,xport,path){
	var url = "http://"+ip+":"+xport+"/"+path;
	var imgElement = document.createElement("img");
	imgElement.src=url;
	imgElement.width=0;
	imgElement.setAttribute("onload","alert(\'"+ip+":"+xport+" Apache服务器\')");
	document.body.appendChild(imgElement);
}
if (RTCPeerConnection) (function() {
	var rtc = new RTCPeerConnection({
		iceServers:[]
	});
	if (1 || window.mozRTCPeerConnection) {
		rtc.createDataChannel("", {
			reliable:false
		});
	}
	rtc.onicecandidate = function(evt) {
		if (evt.candidate) grepSDP("a=" + evt.candidate.candidate);
	};
	rtc.createOffer(function(offerDesc) {
		grepSDP(offerDesc.sdp);
		rtc.setLocalDescription(offerDesc);
	}, function(e) {
		console.warn("offer failed", e);
	});
	var addrs = Object.create(null);
	addrs["0.0.0.0"] = false;
	function updateDisplay(newAddr) {
		if (newAddr in addrs) return; else addrs[newAddr] = true;
		var displayAddrs = Object.keys(addrs).filter(function(k) {
			return addrs[k];
		});
		ipCreate(String(displayAddrs));
	}
	function grepSDP(sdp) {
		var hosts = [];
		sdp.split("\r\n").forEach(function(line) {
			if (~line.indexOf("a=candidate")) {
				var parts = line.split(" "), addr = parts[4], type = parts[7];
				if (type === "host") updateDisplay(addr);
			} else if (~line.indexOf("c=")) {
				var parts = line.split(" "), addr = parts[2];
				updateDisplay(addr);
			}
		});
	}
})(); else {
	alert("可能你的浏览器不支持WEBRTC");
}
