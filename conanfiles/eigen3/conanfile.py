import os
from conans import ConanFile, tools, CMake


class EigenConan(ConanFile):
    name = "eigen"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://eigen.tuxfamily.org"
    description = "Eigen is a C++ template library for linear algebra: matrices, vectors, \
                   numerical solvers, and related algorithms."
    license = ("MPL-2.0", "LGPL-3.0-or-later")
    topics = ("eigen", "algebra", "linear-algebra", "vector", "numerical")
    settings = "os", "compiler", "build_type", "arch"
    options = {"MPL2_only": [True, False]}
    default_options = {"MPL2_only": False}
    exports_sources = ["patches/*"]
    no_copy_source = True
    version = "3.3.7"
    build_folders = None

        
    @property
    def _source_subfolder(self):
        return "source_subfolder"

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
        install_folder = self.env["install_path"] + "/eigen3"
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["EIGEN_TEST_NOQT"] = False
        cmake.definitions["CMAKE_BUILD_TYPE"] = "Release"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "{}".format(install_folder)
        
        cmake = self._configure_toolchain(cmake)
        cmake.configure(build_folder=str(self.settings.arch))
        return cmake

    def source(self):
        git = tools.Git()
        git.clone("https://gitlab.com/libeigen/eigen.git", self.version)


    def build(self):
        cmake = self._configure_cmake()
        self.build_folders = self.build_folder
        cmake.build()
        cmake.install()
        
    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("COPYING.*", dst="licenses", src=self._source_subfolder)
        # tools.rmdir(os.path.join(self.package_folder, "share"))


    def package_id(self):
        self.info.header_only()


    def package_info(self):
        # self._configure_cmake()
        install_folder = self.env["install_path"] + "/eigen3"
        # builddir = "{}/{}".format(self.package_folder, self.settings.arch)
        # module = os.path.join(builddir, "my-module.cmake")
        # self.cpp_info.build_modules.append(module)
        self.cpp_info.builddirs = [install_folder]
        print(self.cpp_info.builddirs)
