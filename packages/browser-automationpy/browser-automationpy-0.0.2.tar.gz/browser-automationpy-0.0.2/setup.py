import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

"""with open('LICENSE.txt') as f:
    license = f.read()"""

setuptools.setup(
    name="browser-automationpy",
    version="0.0.2",
    author="Chandravesh Chaudhari",
    author_email="chandraveshchaudhari@gmail.com",
    description="A python project for easily launching custom automated browser to reduce repetitive boring work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chandraveshchaudhari/browser-automationpy",
    project_urls={
        "Bug Tracker": "https://github.com/chandraveshchaudhari/browser-automationpy/issues",
        'Bug Reports': 'https://github.com/chandraveshchaudhari/browser-automationpy/issues',
        'Say Thanks!': 'https://saythanks.io/to/chandraveshchaudhari',
        'Source': 'https://github.com/chandraveshchaudhari/browser-automationpy/',
    },
    classifiers=["Development Status :: 4 - Beta",
                 "Topic :: Internet :: WWW/HTTP :: Browsers",
                 "Intended Audience :: End Users/Desktop",
                 'Programming Language :: Python :: 3.6',
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 ],
    keywords='browser, automation, selenium, testing, data mining',
    package_dir={"": "src"},
    # license=license,
    install_requires=['selenium',
                      'webdriver-manager'],
    packages=setuptools.find_packages(where="src"),
    # packages=find_packages(exclude=('tests', 'docsrc')),
    python_requires=">=3.6",
)
