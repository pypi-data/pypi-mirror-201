from setuptools import setup

if __name__ == "__main__":
    setup()

# usage of twine:
# pip install twine
# pip uninstall -y sympy.keras && python setup.py install
# del dist\*.tar.gz && python setup.py sdist && twine upload dist/*.tar.gz
# del dist\*.tar.gz && python setup.py sdist && twine upload -r nexus dist/*.tar.gz
# pip uninstall -y sympy.keras && pip install --upgrade sympy.keras
# pip install --upgrade sympy.keras -i https://pypi.Python.org/simple/