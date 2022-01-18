from conans import ConanFile, CMake, tools


class Lz4Conan(ConanFile):
    name = "lz4"
    version = "1.9.1"
    settings = "os", "compiler", "arch", "build_type"
    description = "Conan package for lz4 library"
    url = "https://github.com/lz4/lz4/"
    license = "BSD 2-Clause"
    exports_sources = ["CMakeLists.txt"]

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
        cmake.definitions["CMAKE_BUILD_TYPE"] = "Release"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "{}/{}".format(self.build_folder, self.settings.arch)
        cmake.definitions["CMAKE_CXX_VISIBILITY_PRESET"] = "hidden"
        cmake = self._configure_toolchain(cmake)
        cmake.configure(build_folder=str(self.settings.arch))
        return cmake

    def source(self):
        git = tools.Git(folder="lz4")
        git.clone("https://github.com.cnpmjs.org/lz4/lz4.git", "v{}".format(self.version))

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        
    def package(self):

        self.copy(pattern="*.a", dst="lib", src="{}".format(self.settings.arch))
        self.copy(pattern="lz4.h", dst="include", src="{}/{}/lib/".format(self.source_folder, self.name))


      

        install_folder = self.env["install_path"]

        self.copy(pattern="*.a", dst="{}/lib".format(install_folder), src="{}".format(self.settings.arch))
        self.copy(pattern="lz4.h", dst="{}/include".format(install_folder), src="{}/{}/lib/".format(self.source_folder, self.name))


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
