from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'doodlebob'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    # The root of this section is .pixi/env/defaults
    # not sure what the tuples mean or what surrounding them in square brackets does.
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Parker',
    maintainer_email='parkerg444@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    #Maybe not necessary?
    #extras_require={
    #    'test': [
    #        'pytest',
    #    ],
    #},

    # entry_points. I don't know if this is limited to nodes we run manually or if you need to put them here even if nodes are specified from launch files.
    entry_points={
        'console_scripts': [
            'doodle_test_node = doodlebob.doodle_test_node:main', 
        ],
    },
)
