from setuptools import setup

def get_long_description(path):
    """Opens and fetches text of long descrition file."""
    with open(path, 'r') as f:
        text = f.read()
    return text

setup(
    name = 'CTkMessagebox',
    version = '1.74',
    description = "A modern messagebox for customtkinter",
    license = "Creative Commons Zero v1.0 Universal",
    readme = "README.md",
    long_description = get_long_description('README.md'),
    long_description_content_type = "text/markdown",
    author = 'Akash Bora',
    url = "https://github.com/Akascape/CTkMessagebox",
    package_data = {'': ['*.png']},
    classifiers = [
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords = ['customtkinter', 'customtkinter-dialog', 'customtkinter-messagebox',
                'customtkinter-message-box', 'tkinter-messagebox', 'customtkinter-tkinter-messagebox',
                'messagebox-widget', 'modern-tkinter-messagebox', 'ctkmessagebox'],
    packages = ["CTkMessagebox", "CTkMessagebox.icons"],
    install_requires = ['customtkinter', 'pillow'],
    dependency_links = ['https://pypi.org/project/customtkinter/', 'https://pypi.org/project/Pillow/'],
    python_requires = '>=3.6',
)
