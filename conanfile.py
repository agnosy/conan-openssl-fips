from conans import ConanFile, AutoToolsBuildEnvironment, tools

import os
import tempfile

class OpensslFipsConan(ConanFile):
    name = "OpenSSLFIPS"
    version = "1.0.2t"
    license = "OpenSSL"
    author = "agnosy"
    url = "https://github.com/agnosy/conan-openssl-fips"
    description = "A toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols"
    topics = ("conan", "openssl", "ssl", "tls", "encryption", "security")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = ["src/*"]

    def source(self):
        tools.get("https://www.openssl.org/source/openssl-fips-2.0.16.tar.gz")
        tools.get("https://www.openssl.org/source/openssl-1.0.2t.tar.gz")

    def build(self):
        os.environ["FIPSDIR"] = os.path.join(tempfile.gettempdir(), "ssl", "fips-2.0")
        with tools.chdir(os.path.join(self.source_folder, 'openssl-fips-2.0.16')):
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                self.run("./config")
                self.run("make")
        with tools.chdir(os.path.join(self.source_folder, 'openssl-1.0.2t')):
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                self.run("./config fips")
                self.run("make depend")
                self.run("make")

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join("openssl-fips-2.0.16", "include"))
        self.copy("*.h", dst="include", src=os.path.join("openssl-1.0.2t", "include"))
        self.copy("*ssl.lib", dst="lib", keep_path=False)
        self.copy("*crypto.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("fips_premain.c*", dst="lib", src=os.path.join("openssl-fips-2.0.16", "fips"))
        self.copy("fipscanister.o*", dst="lib", src=os.path.join("openssl-fips-2.0.16", "fips"))
        self.copy("fipsld", dst="bin", src=os.path.join("openssl-fips-2.0.16", "fips"))
        self.copy("fipsld++", dst="bin", src=os.path.join(self.source_folder, "src", "scripts"))
        self.copy("openssl", dst="bin", src=os.path.join("openssl-1.0.2t", "apps"))
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['ssl', 'crypto', 'dl']

