


########## Instructions for updating DDR infrastructure files #################

### Make changes in ddr infrastructure files

cd ~/ddr-home/ddr-clips/ddr-packaging/
edit setup.py for new ddr-clips version number
rm -rf dist
python3 -m build
cp ~/ddr-home/ddr-clips/ddr-packaging/dist/ddr_clips-x.y.z-py3-none-any.whl ddr-home/ddr-clips/infra/xe/infra-files

cd ~/ddr-home/ddr-python/ddr-packaging/
edit setup.py for new ddr-python version number
rm -rf dist
python3 -m build
cp ~/ddr-home/ddr-python/ddr-packaging/dist/ddr_python-x.y.z-py3-none-any.whl ddr-home/ddr-python/infra/xe/infra-files

### Make changes in DDR automation to use the updated ddr-clips and ddr-python packages
### Copy new ddr-clips and ddr-python .whl files

rm ~/ddr-home/ddr-lm/files/xe/infra-files/ddr_*
cp ~/ddr-home/ddr-clips/ddr-packaging/dist/ddr_clips-x.y.z-py3-none-any.whl ~/ddr-home/ddr-lm/files/xe/infra-files
cp ~/ddr-home/ddr-python/ddr-packaging/dist/ddr_python-x.y.z-py3-none-any.whl ~/ddr-home/ddr-lm/files/xe/infra-files

### Edit pipfiles.sh to include new ddr-clips and ddr-python .whl names

~/ddr-home/ddr-lm/files/xe/infra-files/pipfiles.sh

Push changes to ddr-clips repository
Push changes to ddr-python repository
Push changes to ddr-pyats repository

### Make changes in ddr-clips and ddr-python usecases
### Copy selected usecases that will be used with ddr-pyats

cp ~/ddr-home/ddr-clips/usecases/xe/USECASE_Directory ~/ddr-home/ddr-pyats/usecases/xe
cp ~/ddr-home/ddr-python/usecases/xe/USECASE.py ~/ddr-home/ddr-pyats/usecases/xe

### update DDR repositories

git add and git commit changes to repositories and push

~/ddr-home/ddr-clips  git push
~/ddr-home/ddr-python git push
~/ddr-home/ddr-pyats  git push

### update ADS machine DDR repositories
### Assumes that all repositories are stored on ADS in /nobackup/USERNAME/ddr-home...

/nobackup/USERNAME/ddr-home/ddr-clips  git pull
/nobackup/USERNAME/ddr-home/ddr-python git pull
/nobackup/USERNAME/ddr-home/ddr-pyats  git pull


