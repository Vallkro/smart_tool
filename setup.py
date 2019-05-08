from setuptools import find_packages
from setuptools import setup

package_name = 'smart_tool'

setup(
    name=package_name,
    version='0.6.2',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='',
    author_email='',
    maintainer='',
    maintainer_email='',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        '',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description=(
        'Python nodes which were previously in the ros2/examples repository '
        'but are now just used for demo purposes. Now a smart tool, based on the demo_nodes_py'
    ),
    license='',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'listener = smart_tool.topics.listener:main',
            'talker = smart_tool.topics.talker:main',
            'listener_qos = smart_tool.topics.listener_qos:main',
            'talker_qos = smart_tool.topics.talker_qos:main',
            'listener_serialized = smart_tool.topics.listener_serialized:main',
            'mount_client = smart_tool.services.mount_client:main',
            'mount_client_async = smart_tool.services.mount_client_async:main',
            'mount_server = smart_tool.services.mount_server:main'
        ],
    },
)
