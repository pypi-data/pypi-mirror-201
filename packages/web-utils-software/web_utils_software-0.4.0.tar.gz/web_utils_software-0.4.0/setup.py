from setuptools import find_packages, setup

__version__ = "0.4.0"

setup(
    name="web_utils_software",
    version=__version__,
    description="Python Project package",
    long_description="Project to set web utils to get data from the web",
    author="Wilson Ramirez",
    author_email="wil_ramirez02@hotmail.com",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["requests"],
    include_package_data=True,
    # entry_points={
    #     "console_scripts": [
    #         "get-data=src.json_utils:get_json",
    #         "get-image=src.image_utils:get_image",
    #     ]
    # },
)
