from setuptools import setup, find_packages

print(find_packages())

setup(
    name='ChatterAgent',
    version='0.6',
    author='Sevan Brodjian',
    author_email='sevanbro7@gmail.com',
    description='A Python package for spawning agents that interface with the OpenAI ChatGPT API.',
    packages=['ChatterAgent'],
    python_requires='>=3.6',
    url='https://github.com/SevanBrodjian/ChatAgent',
    #py_modules=["ChatterAgent"],
    #package_dir={'':'ChatterAgent'},
    # package_dir = 'src'
)