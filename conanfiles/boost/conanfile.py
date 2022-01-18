from conans import ConanFile, tools


class BoostConan(ConanFile):
    name = "boost"
    version = "1.70.0"
    settings = "os", "compiler", "arch", "build_type"
    description = "Conan package for boost library"
    url = "https://www.boost.org/"
    license = "Boost Software License"
    folder_name = "boost_{}".format(version.replace(".", "_"))

    
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

    def _configure_user_config(self) -> None:
        
        path_to_cxx_compiler = self.env["cxx_compiler_path"]
        
        print("Compiler: {}".format(path_to_cxx_compiler))
        compiler_flags = "-fPIC -std=c++11 "
        user_config = "using gcc : arm : {}\n: <cxxflags>\"{}\"\n;".format(path_to_cxx_compiler, compiler_flags)
        path_to_user_config = "{}/{}/tools/build/src/user-config.jam".format(self.build_folder, self.folder_name)
        file = open(path_to_user_config, "w")
        file.write(user_config)
        file.close()

    def _configure_boost(self) -> None:
        self.run("./bootstrap.sh")

    def _build_boost(self) -> None:
        b2_comd = "./b2 link=static variant=release threading=multi --without-python --debug-configuration --abbreviate-paths architecture={} --stagedir={} target-os=linux".format(self._to_boost_arch(str(self.settings.arch)), self.settings.arch)
        self.run(b2_comd)

    def source(self):
        # "https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/"
        tools.get("https://boostorg.jfrog.io/artifactory/main/release/{}/source/{}.tar.gz".format(self.version, self.folder_name))

    def build(self):
        with tools.chdir(self.folder_name):
            self._configure_user_config()
            self._configure_boost()
            self._build_boost()

    def package(self):
        self.copy(pattern="*.a", dst="lib", src="{}/{}/lib".format(self.folder_name, self.settings.arch))
        self.copy(pattern="*", dst="include/boost", src="{}/boost".format(self.folder_name))
        
        install_folder = self.env["install_path"]
        self.copy(pattern="*.a", dst="{}/lib".format(install_folder), src="{}/{}/lib".format(self.folder_name, self.settings.arch))
        self.copy(pattern="*", dst="{}/include".format(install_folder), src="{}/boost".format(self.folder_name))




    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
