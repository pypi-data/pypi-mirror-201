from setuptools import setup,find_packages

setup(
    name="cubat",
    description="CUBAT  -- CUB Analysis Toolkit",
    version="0.2.0",
    url="https://gxelab.github.io/CUBAT/",
    py_modules=["cubat"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click~=8.0.3","numpy~=1.21.1","pandas~=1.3.0","statsmodels~=0.13.2","setuptools~=66.0.0","biopython~=1.79","click_option_group"],
    entry_points="""
        [console_scripts]
        cubat=cubat.__main__:cli
    """,
    package_data={"example": [ "*.csv"],},
)
