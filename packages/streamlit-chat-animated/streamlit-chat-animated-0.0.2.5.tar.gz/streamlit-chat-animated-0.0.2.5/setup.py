import setuptools

with open('README.md') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="streamlit-chat-animated",
    version="0.0.2.5",
    author="Yash Pravin Pawar, Yash Vardhan Kapil, Darin Manley",
    author_email="darin.j.manley@gmail.com",
    description="A streamlit component, to make chatbots with animated text",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="chat streamlit streamlit-component animated text",
    python_requires=">=3.8",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
