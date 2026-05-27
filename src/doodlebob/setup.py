from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'doodlebob'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    # The root of this section is .pixi/env/defaults
    # Each tuple is (destination, [source_files]).
    # Files are copied into the 
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]), # ROS boilerplate
        ('share/' + package_name, ['package.xml']), # ROS boilerplate
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml'))
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

    # entry_points. These are what launch files refer to when you launch a node
    # and specify the executable. You need an entry here for every node you want to run.
    entry_points={
        'console_scripts': [
            'doodle_test_node = doodlebob.doodle_test_node:main', 
        ],
    },
)
