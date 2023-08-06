from setuptools import setup, find_packages


# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='faciesmapperpro',
      version='2.0.10',
      author='Srv',
      author_email='smukherjee10@slb.com',
      maintainer='Srv',
      maintainer_email='smukherjee10@slb.com',
      description="FaciesMapperPro aims to automate the process of facies interpretation in borehole images using deep learning techniques. \
                    The system is designed to be integrated with Techlog; a software platform developed by SLB for enabling the integration \
                    of all wellbore-centric data types into multi-discipline workflows including geological data analysis.\
                    In 2.0.10 I use concurrent programming and also modify the requirements.txt file for easy installation.",
      packages=['faciesmapperpro'], # NEW: find packages automatically
      install_requires=requirements)