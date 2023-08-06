from setuptools import setup

package_name = "activetune"

install_requires = ["requests"]


if __name__ == "__main__":
    setup(
        install_requires=install_requires,
        packages=[package_name],
        zip_safe=False,
        name=package_name,
        version="0.0.5",
        description="Activetune Python SDK",
    )
