# 前言
这是一个交叉编译仓库，参考了[pcl for android](https://github.com/bashbug/pcl-for-android)，最终生成linux的交叉编译库。

# 使用
1. 修改`conan-profiles/linux`的第8 第9行，设置cxx_compiler_path、c_compiler_path
2. 在终端执行`sh pcl_for_linux/pcl-build-for-linux.sh linux install 0 0` 各参数含义为：
- linux : 表示目标平台，目前只有linux可选。
- install : 最终库安装路径
- 0 0 ： 第一个0 表示是否要重新依赖库源码，第二个0 表示是否要重新编译依赖库
3. 在eaxmple目录下编译，执行：
```
mkdir build
cd build
cmake ..
make -j`nproc`
```
