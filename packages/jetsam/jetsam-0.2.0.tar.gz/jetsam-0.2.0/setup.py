#  ▐▄▄▄▄▄▄ .▄▄▄▄▄.▄▄ ·  ▄▄▄· • ▌ ▄ ·.
#   ·██▀▄.▀·•██  ▐█ ▀. ▐█ ▀█ ·██ ▐███▪
# ▪▄ ██▐▀▀▪▄ ▐█.▪▄▀▀▀█▄▄█▀▀█ ▐█ ▌▐▌▐█·
# ▐▌▐█▌▐█▄▄▌ ▐█▌·▐█▄▪▐█▐█ ▪▐▌██ ██▌▐█▌
#  ▀▀▀• ▀▀▀  ▀▀▀  ▀▀▀▀  ▀  ▀ ▀▀  █▪▀▀▀
from setuptools import setup, Extension
import platform

with open("README.md", "r") as f:
    long_desc = f.read()

define = "__BOGUS__"
system = platform.system()

if system == "Darwin":
    define = "_DARWIN_C_SOURCE"
elif system == "Linux":
    define = "__USE_MISC"


setup(
    name="jetsam",
    version="0.2.0",
    description="Jettison functions with jetsam!",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Tony B",
    author_email="tony@ballast.dev",
    license="MIT",
    license_files=["LICENSE"],
    ext_modules=[
        Extension(
            name="detacher",
            sources=["src/detach.c", "src/log.c"],
            include_dirs=["src/"],  # this is broken, need MANIFEST.in
            define_macros=[(define, None)],
        )
    ],
    package_dir={"": "src/"},
    # since package_dir is set, no automatic discovery
    py_modules=["jetsam"],
    project_urls={"Source Code": "https://gitlab.com/ballast-dev/jetsam"},
    python_requires=">=3.8",
)
