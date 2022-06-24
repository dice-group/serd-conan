import os

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conans.util.files import rmdir

required_conan_version = ">=1.33.0"


class Recipe(ConanFile):
    name = "serd"
    version = "0.30.13-f6437f"
    homepage = "https://gitlab.com/drobilla/serd.git"
    description = "A lightweight C library for RDF syntax"
    topics = "linked-data", "semantic-web", "RDF", "turtle", "TriG", "NTriples", "NQuads"
    author = "David Robillard <d@drobilla.net>"
    scm = {
        "type": "git",
        "url": "https://gitlab.com/drobilla/serd.git",
        "revision": "f6437f606bd85dbc6d7581146955f85902230ca0",
        "submodule": "recursive"
    }
    settings = "build_type", "compiler", "os", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }
    license = "ISC"
    generators = "cmake_find_package"
    exports_sources = "src*", "include*", "doc*", "waf", "wscript", "waflib*", "serd.pc.in"

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def validate(self):
        if self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("Don't know how to setup WAF for VS.")

    def build(self):
        args = ["--no-utils", " --prefix={}".format(self.folders.package_folder)]
        if not self.options["shared"]:
            args += ["--static", "--no-shared"]
        if self.options["fPIC"]:
            args += ["-fPIC"]
        args = " ".join(arg for arg in args)

        cflags = []
        print(self.settings.build_type == "Release")
        if self.settings.build_type in ["Debug", "RelWithDebInfo"]:
            cflags += ["-g"]
        if self.settings.build_type in ["Release", "RelWithDebInfo"]:
            cflags += ["-O3"]
        if self.settings.build_type in ["Release", "MinSizeRel"]:
            cflags += ["-DNDEBUG"]
        if self.settings.build_type == "MinSizeRel":
            cflags += ["-Os"]
        cflags = " ".join(cflag for cflag in cflags)

        self.run(f'CFLAGS="{cflags}" ./waf configure {args}')
        self.run('./waf build')

    def package(self):
        self.run('./waf install')
        rmdir(os.path.join(self.package_folder, "share"))
        rmdir(os.path.join(self.package_folder, "lib/pkgconfig"))
        self.copy("COPYING", src=self.folders.base_export_sources, dst="licenses")

    def package_info(self):
        libname = "{}-0".format(self.name)
        self.cpp_info.libs = [libname]
        self.cpp_info.includedirs = [f"include/{libname}/"]
        self.cpp_info.cflags = ["-std=c11"]
