#!/bin/bash
cd ..

MESSAGE=$1
VERSION=`grep __version__ fgmk/__init__.py | cut -d= -f2 | tr -d '[[:space:]]'`

if [[ -z "$MESSAGE" ]]
then

  echo "empty tag message... Aborting."
  echo ''
  echo "please use ./ReleaseToPypi.sh MESSAGE"
  echo ''
  exit 1
fi

echo ''
echo "git tag message is: $MESSAGE"
echo ''
echo "fgmk version is: $VERSION"

read -p "press any key to continue " -n 1 -r


read -p "Should we add this tag? " -n 1 -r
echo  ''
if [[ $REPLY =~ ^[Yy]$ ]]
then

  git tag $VERSION -m "$MESSAGE"
  git push --tags origin master

  python3 setup.py sdist
  LATESTDIST=`ls -td dist/* | head -1`

  echo "the distributable is: $LATESTDIST"
  read -p "press any key to continue " -n 1 -r
  read -p "Should we upload to PyPI? " -n 1 -r
  echo  ''
  if [[ $REPLY =~ ^[Yy]$ ]]
  then

    twine register $LATESTDIST
    twine upload dist/$LATESTDIST

  fi

fi
