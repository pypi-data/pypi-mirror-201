"""Build C++ module for poetry."""

import os
import pathlib
import subprocess
import sys

import setuptools
import setuptools.command.build_ext
import toml

THIS_DIR = pathlib.Path(__file__).absolute().parent


class CMakeExtension(setuptools.Extension):
    """CMake extensions."""

    def __init__(self, name: str) -> None:
        super().__init__(name=name, sources=[])


class ExtensionBuilder(setuptools.command.build_ext.build_ext):
    """Builder of extensions."""

    def build_extension(self, ext: setuptools.Extension) -> None:
        if not isinstance(ext, CMakeExtension):
            super().build_extension(ext)

        lib_root_dir = (
            pathlib.Path.cwd() / self.get_ext_fullpath("num_collect")
        ).parent.resolve()

        source_dir = str(THIS_DIR)
        build_dir = f"{self.build_temp}/cpp_module"
        build_type = "Release"

        os.makedirs(build_dir, exist_ok=True)

        # Add Conan remotes.
        subprocess.run(
            [
                "conan",
                "remote",
                "add",
                "-f",
                "cpp-hash-tables",
                "https://gitlab.com/api/v4/projects/35726343/packages/conan",
            ],
            check=True,
        )
        subprocess.run(
            [
                "conan",
                "remote",
                "add",
                "-f",
                "numerical-collection-cpp",
                "https://gitlab.com/api/v4/projects/25109105/packages/conan",
            ],
            check=True,
        )

        # Install Conan packages.
        subprocess.run(
            [
                "conan",
                "install",
                "--build",
                "missing",
                "-s",
                f"build_type={build_type}",
                source_dir,
            ],
            cwd=build_dir,
            check=True,
        )

        # Build.
        subprocess.run(
            [
                "cmake",
                # cspell: ignore DBUILD, DPYTHON, DNUM
                f"-DCMAKE_BUILD_TYPE={build_type}",
                f"-DPYTHON_EXECUTABLE={sys.executable}",
                f"-DNUM_COLLECT_PY_ROOT={lib_root_dir}",
                source_dir,
            ],
            cwd=build_dir,
            check=True,
        )
        subprocess.run(
            [
                "cmake",
                "--build",
                ".",
                "--config",
                build_type,
            ],
            cwd=build_dir,
            check=True,
        )


def read_file(filepath: str) -> str:
    """Read all lines in a file."""
    with open(filepath, mode="r", encoding="utf8") as file:
        return file.read()


pyproject_toml = toml.load(str(THIS_DIR / "pyproject.toml"))
pyproject_toml_tool_poetry = pyproject_toml["tool"]["poetry"]

package_list = setuptools.find_packages(exclude=["tests*"])
package_data = {name: ["py.typed"] for name in package_list}
package_data.update({"num_collect._cpp_module": ["num_collect_py_cpp_module*"]})

# Reference of keywords:
# https://setuptools.pypa.io/en/latest/references/keywords.html
setuptools.setup(
    name=pyproject_toml_tool_poetry["name"],
    version=pyproject_toml_tool_poetry["version"],
    description=pyproject_toml_tool_poetry["description"],
    long_description=read_file(str(THIS_DIR / "README.md")),
    long_description_content_type="text/markdown",
    author="Kenta Kabashima",
    author_email="kenta_program37@hotmail.co.jp",
    url=pyproject_toml_tool_poetry["homepage"],
    classifiers=pyproject_toml_tool_poetry["classifiers"],
    license=pyproject_toml_tool_poetry["license"],
    ext_modules=[
        CMakeExtension(
            name="num_collect._cpp_module.num_collect_py_cpp_module",
        )
    ],
    cmdclass={"build_ext": ExtensionBuilder},  # cspell: disable-line
    zip_safe=False,
    packages=package_list,
    include_package_data=False,
    package_data=package_data,
    python_requires=pyproject_toml["tool"]["poetry"]["dependencies"]["python"],
    install_requires=["numpy>=1.24.2,<2.0"],
)
