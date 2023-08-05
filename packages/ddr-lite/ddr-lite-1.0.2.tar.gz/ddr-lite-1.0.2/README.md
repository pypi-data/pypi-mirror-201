#
# Instructions to build and publish updated ddr-lite
#
# 1. Edit ddr-lite/ddr-packaging/setup.py with new version number
# 2. rm -rf ddr-lite/ddr-packaging/dist
# 3. Run following commands in: ddr-lite/ddr-packaging
 
pip3 install build
pip3 install twine
pip3 install wheel
python3 -m build
python3 -m twine upload --repository pypi dist/* --verbose 
