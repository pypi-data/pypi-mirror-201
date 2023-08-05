from setuptools import setup, find_packages

setup(name='prototyping_inference_engine',
      packages=["prototyping_inference_engine"],
      py_modules=["prototyping_inference_engine.*"],
      package_data={'': ['*.lark', '*.dlgp']},
      include_package_data=True)




