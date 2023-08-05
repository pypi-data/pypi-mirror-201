import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='noteyXMLParser',  
     version='0.2.1',
     author="Amin Mahjoub",
     author_email="mahjoub@usc.edu",
     description="Music XML Parser",
     long_description=long_description,
     package_dir={"":"/Users/aminmahjoub/NoteyXMLParser/xmlParser/src"},
     url="https://github.com/mmahjoub5/NoteyXMLParser",
   long_description_content_type="text/markdown",
     packages=['noteyXMLParser'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )