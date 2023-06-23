

注意事项：
- 启动Django: .vscode/launch.json
- 使用前请先设置本地代理：index/utils/CodeGeneration.py中的set_proxy()函数
- 配置文件：index/utils/config/default.json
- 要用gpt3.5，需要把index/views.py中的所有演示用的代码注释掉，把其他注释掉的代码解开注释


存在的问题：
- api调用的GPT和ChatGPT差距还是比较大，效果感觉差一点，但是稳定一点；一般都不会出现生成截断的情况
- 将生成的代码解析成文件（Code_Parsing使用正则匹配进行HTML\CSS\JS解析）有时会出错


成功示例：
- Please generate a frontend code which implements a drawing application based on the HTML5 canvas element, allowing users to draw on the canvas, adjust brush size, select colors, and clear the canvas.
- Please generate a to-do list page where users can add, mark as completed and delete to-do items.



图片来源：
https://unsplash.com/

https://images.unsplash.com/photo-1547756536-cde3673fa2e5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8SGFycnklMjBQb3R0ZXJ8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60

https://via.placeholder.com/100


演示记录:

Please generate a web page with a random roll call function.

In this scenario, there are two lists: a list of people and a list of people who have requested leave. The task is to perform a random roll call process, but the people on the leave list should be excluded from the roll call. The remaining people who are not on leave should be included in the roll call.

I need a function: when some people ask for leave, I can have an exclusion list to exclude these people in the random roll call process.

Please blur the background of the page.

Please blur the text box of the page.

Code

Code_Modification

Frank

