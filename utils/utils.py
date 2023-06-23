import os
import zipfile


def zip_folder(folder_path, output_path):
    # 创建zip文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 遍历文件夹中的所有文件和子文件夹，并压缩它们
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))



def iframe_generator(file_path):
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
    
    return iframe