# 说明

这个模块是用于包装 artistml-skill 中的 workflow 的，步骤如下

1. 找到 artistml-skill 中的所有子目录，里面有 main.py 文件的即是需要进行包装的文件
2. 找到文件中的 run 函数，然后给文件尾部添加直接调用 run 函数的方法
3. 根据 skills 下面的 yaml 文件，找到entrypoint中需要的所有子节点名，组装一个 workflow template 并提交到 argo 集群
4. 根据 template 的名字，可以使用 hacker 的 api 获得请求体参数
