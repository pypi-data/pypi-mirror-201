from setuptools import setup, find_packages

setup(
    name='burst',
    version='3.1.37',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    python_requires='>=3',
    scripts=['burst/bin/burstctl'],
    install_requires=['setproctitle', 'twisted', 'events', 'netkit', 'click'],
    url='https://github.com/dantezhu/burst',
    license='MIT',
    author='dantezhu',
    author_email='zny2008@gmail.com',
    description='twisted with master, proxy and worker',
)
