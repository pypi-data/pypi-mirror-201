#!/bin/bash
# Clean and Prepare. Must be ran from the root of this repo
WORKING_DIR="./package"
if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi

mkdir -p ./package/oak9/tython

# Copy all directories and files to package directory
cp runner.py ./package/oak9/tython
rsync -R -r -v ./models ./package/oak9/tython
rsync -R -r -v ./core ./package/oak9/tython

# #Fix imports
# cp ./python/post-generate-clean.py ./package
# pushd ./package

# python ./post-generate-clean.py

# popd

#Create init
cp ./python/gen_init.py ./package

pushd ./package

python ./gen_init.py

popd

# Add in module and package definitions
for file in $(find ./package/oak9 -type d | uniq); do cp ./python/proto-init-file.py ${file}/__init__.py; done
cp ./python/runner-setup.py ./package/setup.py

# Shows the disk usage of package items
du -sh *

pushd ./package

# Create Package, run with bash
python ./setup.py sdist bdist_wheel

popd