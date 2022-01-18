from conans import ConanFile, CMake, tools
import os

class FlannConan(ConanFile):
    name = "flann"
    version = "1.9.1"
    settings = "os", "compiler", "arch", "build_type"
    description = "Conan package for flann library"
    url = "http://www.cs.ubc.ca/research/flann/"
    license = "BSD"

    def _to_android_arch(self, arch: str) -> str:
        if arch == "armv7": return "armv7a"
        if arch == "armv8": return "aarch64"
        if arch == "linux": return "aarch64"
        else : return None
        return arch

    def _to_android_address_model(self, arch: str) -> str:
        if arch == "armv7": return "32"
        if arch == "armv8" or arch == "x86_64": return "64"
        return None

    def _to_boost_arch(self, arch: str) -> str:
        if arch.startswith("arm") or arch == "aarch64": return "arm"
        if arch.startswith("x86"): return "x86"
        else: return "aarch64"
        return None

    def _to_android_platform(self, api_level: str) -> str:
        return "android-{}".format(api_level)

    def _configure_toolchain(self, cmake):
        
        cmake.definitions["CMAKE_CXX_COMPILER"] = self.env["cxx_compiler_path"]
        cmake.definitions["CMAKE_C_COMPILER"] = self.env["c_compiler_path"]
 
        return cmake

    def _configure_cmake(self):
        cmake = CMake(self)
        install_folder = self.env["install_path"] + "/flann"
        cmake.definitions["CMAKE_BUILD_TYPE"] = "Release"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "{}/{}".format(self.build_folder, self.settings.arch)
        cmake.definitions["CMAKE_CXX_VISIBILITY_PRESET"] = "hidden"
        cmake.definitions["BUILD_C_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_PYTHON_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_MATLAB_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_DOC"] = "OFF"
        cmake = self._configure_toolchain(cmake)
        cmake.configure(build_folder=str(self.settings.arch))
        return cmake

    def requirements(self):
        self.requires("lz4/1.9.1@bashbug/stable")

    def source(self):
        git = tools.Git()
        git.clone("https://github.com.cnpmjs.org/flann-lib/flann.git", self.version)
        print("fix flann repo: https://stackoverflow.com/questions/50763621/building-flann-with-cmake-fails")
        os.system("touch src/cpp/empty.cpp")
        os.system('sed -i "32c add_library(flann_cpp SHARED empty.cpp)" src/cpp/CMakeLists.txt')
        os.system('sed -i "86c add_library(flann SHARED empty.cpp)" src/cpp/CMakeLists.txt')

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="*.a", dst="lib", src="{}/lib".format(self.settings.arch))
        # add lz4 as transtive dependency
        self.run("cp {}/liblz4.a {}/lib".format(self.deps_cpp_info["lz4"].lib_paths[0], self.package_folder))
        self.copy(pattern="*", dst="include", src="{}/include".format(self.settings.arch))


        install_folder = self.env["install_path"] + "/flann"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = install_folder
        cmake.configure(build_folder=str(self.settings.arch))
        cmake.install()

        install_folder = self.env["install_path"]
        self.copy(pattern="*.a", dst="{}/lib".format(install_folder), src="{}/lib".format(self.settings.arch))
        # add lz4 as transtive dependency
        self.run("cp {}/liblz4.a {}/lib".format(self.deps_cpp_info["lz4"].lib_paths[0], install_folder))
        self.copy(pattern="*", dst="{}/include".format(install_folder), src="{}/include".format(self.settings.arch))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
