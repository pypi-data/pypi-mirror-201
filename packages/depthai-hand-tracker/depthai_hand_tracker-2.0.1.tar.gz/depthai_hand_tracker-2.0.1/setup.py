import setuptools
import glob
data_files = []
directories = ['custom_models', 'models']
for directory in directories:
    files = glob.glob(directory+'/*.blob')
    data_files.append(("depthai_hand_tracker", files))
setuptools.setup(name='depthai_hand_tracker',
long_description='Publishing to used as public dependency',
version='2.0.1',
description='Depthai Hand Tracker',
url='https://github.com/geaxgx/depthai_hand_tracker',
author='geaxgx',
install_requires=['opencv-python>= 4.5.1.48', 'depthai>=2.13'],
author_email='',
packages=setuptools.find_packages(),
include_package_data=True,
package_data={'': ['*.blob']},
zip_safe=False)