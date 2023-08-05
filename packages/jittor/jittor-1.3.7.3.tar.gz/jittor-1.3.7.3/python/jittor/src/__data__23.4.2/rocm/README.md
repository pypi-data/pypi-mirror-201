# rocm-jittor

### 编译方法：

1. 进入 jittor 目录，将 rocm_jittor.cc 拷贝至 `python/jittor/extern/rocm/rocm_jittor.cc`
2. 对于 RedHat-7 及以下 OS，gcc 默认不使用 cxx11 abi，因此运行以下命令得到 `python/jittor/extern/rocm/rocm_cache.o`
```
g++ python/jittor/extern/rocm/rocm_jittor.cc -Wall -Wno-unknown-pragmas -std=c++14 -fPIC  -march=native  -fdiagnostics-color=always  -lstdc++ -ldl -I"python/jittor/src" -I"python/jittor/extern/rocm" -c -o "python/jittor/extern/rocm/rocm_cache.o"
```
3. 对于其他 OS，gcc 默认使用 cxx11 abi，因此运行以下命令得到 `python/jittor/extern/rocm/rocm_cache_cxx11.o`
```
g++ python/jittor/extern/rocm/rocm_jittor.cc -Wall -Wno-unknown-pragmas -std=c++14 -fPIC  -march=native  -fdiagnostics-color=always  -lstdc++ -ldl -I"python/jittor/src" -I"python/jittor/extern/rocm" -c -o "python/jittor/extern/rocm/rocm_cache_cxx11.o"
```

4. 在两者环境下编译得到 o 文件后，将其打包为 `python/jittor/extern/rocm/rocm_cache.tar.gz`
```
tar -czvf rocm_cache.tar.gz rocm_cache.o rocm_cache_cxx11.o
```


### 曙光集群环境配置方法

1. 跳板机申请资源 `salloc -p kshdtest -n 4 --gres=dcu:4 --exclusive`（不能申请单卡，驱动有问题）
2. ssh 到计算节点
3. 设置 module

```
module rm compiler/rocm/2.9
module load apps/python/3.8.10
module load compiler/rocm/dtk-21.10.1
```
