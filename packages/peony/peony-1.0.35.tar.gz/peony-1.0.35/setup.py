from setuptools import setup, find_packages

setup(
    name='peony',
    version='1.0.35',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    python_requires='>=3',
    scripts=['peony/bin/peonyctl'],
    install_requires=['maple>=4.0.0', 'setproctitle', 'twisted', 'events', 'netkit', 'click', 'pyglet'],
    url='https://github.com/dantezhu/peony',
    license='MIT',
    author='dantezhu',
    author_email='zny2008@gmail.com',
    description='',
)
