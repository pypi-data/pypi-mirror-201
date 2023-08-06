#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name="macrometa-target-snowflake",
      version='0.0.12',
      description="Macrometa target for loading data to Snowflake",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Macrometa",
      url='https://github.com/Macrometacorp/macrometa-target-snowflake',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
      py_modules=["macrometa_target_snowflake"],
      python_requires='>=3.7',
      install_requires=[
          'pipelinewise-singer-python==1.2.0',
          'snowflake-connector-python[pandas]==2.7.*',
          'inflection==0.5.1',
          'joblib==1.2.0',
          'boto3==1.23.10',
          'c8connector==0.0.15'
      ],
      extras_require={
          "test": [
              "pylint==2.12.*",
              'pytest==7.0.1',
              'pytest-cov==4.0.0',
              "python-dotenv==0.19.*"
          ]
      },
      entry_points="""
          [console_scripts]
          macrometa-target-snowflake=macrometa_target_snowflake:main
      """,
      packages=['macrometa_target_snowflake', 'macrometa_target_snowflake.file_formats',
                'macrometa_target_snowflake.upload_clients']
      )
