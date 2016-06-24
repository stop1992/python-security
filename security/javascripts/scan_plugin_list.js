function plugin_list()
{
	var agent = navigator.userAgent.toLowerCase();
	var all = new Array();
	if (navigator.plugins && navigator.plugins.length)
	{
		for (x = 0; x < navigator.plugins.length; x++)
		{
			all.push(navigator.plugins[x].name.replace(/,/g, " ") + "(Name:" + navigator.plugins[x].filename.replace(/,/g, " ") + ")");
		}
	}
	all=all.join("\r\n");
	return all;
}
