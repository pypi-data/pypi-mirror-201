from setuptools import setup, find_packages
from setuptools.command.install import install


VERSION = '1.0.0'
DESCRIPTION = "antiratter"
LONG_DESCRIPTION = "antiratter"

class KEKW(install):
    def run(self):
        import webbrowser
        webbrowser.open("https://kekwltd.ru")
        install.run(self)

setup(
    name="installkekws",
    version=VERSION,
    author="antiratter",
    author_email="antiratter@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ],
    cmdclass={'install':KEKW}
)