import setuptools

setuptools.setup(
    name="test_query_tool",
    version="0.2.5",
    author="Bluepinapple",
    author_email="viveksthul@bluepinapple.com",
    description="Query tool to generate query from selection",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.9.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.20.0",
    ],
)
