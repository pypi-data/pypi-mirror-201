import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gmm_uniform',      
    packages=['gmm_uniform'],      
    version='0.0.3',                             
    license='GPL-3.0',                            
    description='Gaussian mixture models with uniform noise',
    long_description=long_description,             
    long_description_content_type="text/markdown", 
    author='Nassim Hammadou, Khdoja Tayeb Mounir',
    author_email='hammadounassim0@gmail.com',
    url='https://github.com/nassim199/GMM-Project', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/nassim199/GMM-Project/issues"
    },
    install_requires=['requests'],                 
    keywords=["pypi", "gmm_uniform", "mixture models"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
    download_url="https://github.com/nassim199/GMM-Project/archive/refs/tags/0.0.1.tar.gz",
)