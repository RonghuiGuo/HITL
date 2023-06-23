file_path = "123"
iframe = """
        <iframe src="file={0}" id="bi_iframe" width="100%" height="500px" onload="adjustIframe();"></iframe>
        <script>
        function adjustIframe(){{
            var ifm= document.getElementById("bi_iframe");
            ifm.height=document.documentElement.clientHeight;
            ifm.width=document.documentElement.clientWidth;
        }}
        </script>
        """.format(file_path)

print(iframe)
