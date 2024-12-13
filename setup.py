#!/usr/bin/env python
# SPDX-License-Identifier: EUPL-1.2
#
# (C) Copyright 2018-2024 CSI-Piemonte

from setuptools import setup
from setuptools.command.install import install as _install


class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()


def load_requires():
    with open("./MANIFEST.md") as f:
        requires = f.read()
    return requires


def load_version():
    with open("./bee_client/VERSION") as f:
        version = f.read()
    return version


if __name__ == "__main__":
    version = load_version()
    setup(
        name="bee_client",
        version=version,
        description="Platform client",
        long_description="Platform client",
        author="CSI Piemonte",
        author_email="nivola.engineering@csi.it",
        license="EUPL-1.2",
        url="",
        scripts=[],
        packages=[
            "bee_client",
        ],
        namespace_packages=[],
        py_modules=["bee_client.__init__"],
        classifiers=[
            "Development Status :: %s" % version,
            "Programming Language :: Python",
        ],
        entry_points={},
        data_files=[],
        package_dir={"bee_clinet": "bee_client"},
        package_data={"bee_client": ["VERSION"]},
        install_requires=load_requires(),
        dependency_links=[],
        zip_safe=True,
        cmdclass={"install": install},
        keywords="",
        python_requires="",
        obsoletes=[],
    )
