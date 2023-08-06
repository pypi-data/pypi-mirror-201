from setuptools import find_packages, setup

setup(
    name='mqttSSOP',
    packages=find_packages(include=['clientPublisher','clientSubscriber']),
    version='0.1.0',
    description='Mqtt library in SSOP project',
    author='Pedro Vila Luz',
    license='Tecnico ULisboa',
    install_requires=['pip install paho-mqtt'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)