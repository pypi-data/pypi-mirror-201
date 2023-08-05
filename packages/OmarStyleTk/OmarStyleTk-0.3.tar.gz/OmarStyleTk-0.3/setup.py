
import setuptools
with open('README.md', 'r') as fh:
    long_description = fh.read()
# with open('requirements.txt','r') as fr:
#     requires = fr.read().split('\n')

setuptools.setup(
    name='OmarStyleTk',
    version="0.3",
    author='omar Style',
    author_email='omarllStyle@gmail.com',
    description='Omar_Style _ 〄🇵🇸',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Omarail1/omarpoop.git',
    packages=['OmarStyleTk'],
    install_requires=["requests","Pillow","datetime"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License'],
    
   
)