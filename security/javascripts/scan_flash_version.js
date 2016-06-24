function flashver() {
	var flash = function() {};
	flash.prototype.controlVersion = function() {
		var version;
		var axo;
		var e;
		try {
			axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");
			version = axo.GetVariable("$version")
		} catch(e) {}
		if (!version) {
			try {
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");
				version = "WIN 6,0,21,0";
				axo.AllowScriptAccess = "always";
				version = axo.GetVariable("$version")
			} catch(e) {}
		}
		if (!version) {
			try {
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
				version = axo.GetVariable("$version")
			} catch(e) {}
		}
		if (!version) {
			try {
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.3");
				version = "WIN 3,0,18,0"
			} catch(e) {}
		}
		if (!version) {
			try {
				axo = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
				version = "WIN 2,0,0,11"
			} catch(e) {
				version = -1
			}
		}
		var verArr = version.toString().split(",");
		var str = "";
		for (var i = 0,
				l = verArr.length; i < l; i++) {
					if (verArr[i].indexOf("WIN") != -1) {
						str += verArr[i].substring(3);
						str += "."
					} else {
						if (i == (l - 1)) {
							str += verArr[i]
						} else {
							str += verArr[i];
							str += "."
						}
					}
				}
		return (str)
	};
	flash.prototype.getSwfVer = function() {
		var isIE = (navigator.appVersion.indexOf("MSIE") != -1) ? true: false;
		var isWin = (navigator.appVersion.toLowerCase().indexOf("win") != -1) ? true: false;
		var isOpera = (navigator.userAgent.indexOf("Opera") != -1) ? true: false;
		var flashVer = -1;
		if (navigator.plugins != null && navigator.plugins.length > 0) {
			if (navigator.plugins["Shockwave Flash 2.0"] || navigator.plugins["Shockwave Flash"]) {
				var swVer2 = navigator.plugins["Shockwave Flash 2.0"] ? " 2.0": "";
				var flashDescription = navigator.plugins["Shockwave Flash" + swVer2].description;
				var descArray = flashDescription.split(" ");
				var tempArrayMajor = descArray[2].split(".");
				var versionMajor = tempArrayMajor[0];
				var versionMinor = tempArrayMajor[1];
				var versionRevision = descArray[3];
				if (versionRevision == "") {
					versionRevision = descArray[4]
				}
				if (versionRevision[0] == "d") {
					versionRevision = versionRevision.substring(1)
				} else {
					if (versionRevision[0] == "r") {
						versionRevision = versionRevision.substring(1);
						if (versionRevision.indexOf("d") > 0) {
							versionRevision = versionRevision.substring(0, versionRevision.indexOf("d"))
						}
					}
				}
				var flashVer = versionMajor + "." + versionMinor + "." + versionRevision
			}
		} else {
			if (navigator.userAgent.toLowerCase().indexOf("webtv/2.6") != -1) {
				flashVer = 4
			} else {
				if (navigator.userAgent.toLowerCase().indexOf("webtv/2.5") != -1) {
					flashVer = 3
				} else {
					if (navigator.userAgent.toLowerCase().indexOf("webtv") != -1) {
						flashVer = 2
					} else {
						if (isIE && isWin && !isOpera) {
							flashVer = new flash().controlVersion()
						}
					}
				}
			}
		}
		return flashVer
	};
	if (flash.prototype.getSwfVer() == -1) {
		return "No Flash!"
	} else {
		return "Shockwave Flash " + flash.prototype.getSwfVer()
	}
}
alert(flashver());
