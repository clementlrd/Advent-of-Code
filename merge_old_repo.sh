#! /bin/bash

# This script do the following:
# - Add an extern repository <old_repo> into this one in a folder named <folder_name>
# - It creates a branch with the same name as the folder (<folder_name>)
# - It merges the history commit of the old repository into the newly created branch
#
# To have the same history track that I've done in this repository, remove the merge commit
# by creating a temporary branch on the commit just before the merge commit,
# before deleting the branch <folder_name>. When the branch is ready to be merged:
# `git checkout main && git merge --squash --ff <folder_name>`
#
# Inspired from:
# - https://stackoverflow.com/questions/1425892/how-do-you-merge-two-git-repositories
# - https://gist.github.com/x-yuri/9890ab1079cf4357d6f269d073fd9731

if [ $# -ne 2 ] 
then
  echo Please enter args as follow:
  echo "    merge_old_repo.sh <old_repo_path> <folder_name>"
  exit
fi

OLD_REPO=$1
NEW_FOLDER=$2

BRANCH=$2
REMOTE=remote-$2

# verbose
set -eux

# create a copy to modify git history
cp -r $OLD_REPO $NEW_FOLDER

# rework the history to be inside the folder
(
  cd $NEW_FOLDER
  time git filter-repo --to-subdirectory-filter $NEW_FOLDER --force
)

# switch to the commit before the merge
git checkout main
# add old repo as remote
git remote add $REMOTE $NEW_FOLDER
# retrieve content from git history
git fetch $REMOTE --no-tags
# create a new branch for the repository
git switch -c $BRANCH
# merge to the newly created branch
EDITOR=true git merge --allow-unrelated-histories $REMOTE/master

# remove temporary remote
git remote remove $REMOTE
# remove temporary clone
rm -rf $NEW_FOLDER/$NEW_FOLDER
# remove old .git
rm -rf $NEW_FOLDER/.git