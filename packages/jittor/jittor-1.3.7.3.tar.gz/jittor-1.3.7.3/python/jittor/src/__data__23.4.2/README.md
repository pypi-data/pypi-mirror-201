# Jittor BY repo

这个仓库包含了计图的BY代码, 如果需要修改BY代码, 可以通过以下方式完成:

```bash
cd {jittor_path}/src
git clone https://github.com/jittor-online-first/__data__.git
export use_data_gz=0
```

把 `__data__` 仓库 clone 到 src 目录下并且设置环境变量以后, 
jittor就会自动编译这些代码, 而不是下载已经编译好的混淆代码.

如果要把改好的 `__data__` 代码上线, 需要先编译好混淆代码, 混淆代码的生成方式为：

```bash
python3.7 ./src_obfuse.py
```

这个命令会在jittor的utils目录下生成`data.gz`文件，包含了咱们的混淆代码，
混淆代码脚本目前使用的是比较简单的字符串替换混淆，可能会混淆不成功，如果识别不成功，
可能是全局token识别错误，可以修改全局token表，参考`src_obfuse.py`源码。
用下面代码检查是否混淆成功：

```bash
use_data_gz=1 python3.7 -m jittor.test.test_core
```

成功后，commit&push主仓库和by仓库即可。