#!/bin/bash

set -e

PROFILE="linux"
PWD=$(cd $(dirname $0); pwd)
INSTALL_PATH="${PWD}/install"
KEEP_SOURCE=""
KEEP_BUILD=""
if [ $# -ge 1 ]; then
  PROFILE=${1}
fi 

if [ $# -ge 2 ]; then
  if [ ${2:0:1} == "/" ]; then
    INSTALL_PATH=${2}
  else
    INSTALL_PATH="${PWD}/${2}"
  fi
fi 

if [ $# -ge 3 ]; then
  if [ ${3} = '1' ]; then
    KEEP_SOURCE="--keep-source"
  else
    KEEP_SOURCE=""
  fi
fi 

if [ $# -ge 4 ]; then
  if [ ${4} = '1' ]; then
    KEEP_BUILD="--keep-build"
  else
    KEEP_BUILD=""
  fi
fi 


$(sed -i "10c install_path=${INSTALL_PATH}" conan-profiles/${PROFILE})


echo -e "\n\n\033[1;32m###########################################"
echo -e "Build args\n"
echo -e "profile: ${PROFILE}"
echo -e "install path: ${INSTALL_PATH} "
echo -e "keep source: ${KEEP_SOURCE} "
echo -e "keep build: ${KEEP_BUILD} "
echo -e "###########################################\033[m\n\n"



echo -e "\n\n\033[1;35m###########################################"
echo -e "### FLANN cross-compiling start...      ###"
echo -e "###########################################\033[m\n\n"


conan create -pr conan-profiles/${PROFILE} conanfiles/lz4 bashbug/stable ${KEEP_SOURCE} ${KEEP_BUILD}
conan create -pr conan-profiles/${PROFILE} conanfiles/flann bashbug/stable ${KEEP_SOURCE} ${KEEP_BUILD}

echo "FLANN cross-compiling finished!"

echo -e "\n\n\033[1;35m###########################################"
echo -e "### BOOST cross-compiling start...      ###"
echo -e "###########################################\033[m\n\n"

conan create -pr conan-profiles/${PROFILE} conanfiles/boost bashbug/stable  ${KEEP_SOURCE} ${KEEP_BUILD}

echo "BOOST cross-compiling finished!"


echo -e "\n\n\033[1;35m###########################################"
echo -e "### Eigen3 cross-compiling start...      ###"
echo -e "###########################################\033[m\n\n"

conan create -pr conan-profiles/${PROFILE} conanfiles/eigen3 bashbug/stable  ${KEEP_SOURCE} ${KEEP_BUILD}

echo "Eigen3 cross-compiling finished!"

echo -e "\n\n\033[1;35mm###########################################"
echo -e "### PCL cross-compiling start...        ###"
echo -e "###########################################\033[m\n\n"

echo -e "\n\n\033[1;32m this will run for a while... time to drink a\n"
echo -e "   ( ( "
echo -e "    ) ) "
echo -e "  ........ "
echo -e "  |      |] "
echo -e "  \      /  "
echo -e "   '----' \033[m\n\n"

conan create -pr conan-profiles/${PROFILE} conanfiles/pcl bashbug/stable ${KEEP_SOURCE} ${KEEP_BUILD}

cp conan-profiles/${PROFILE} ~/.conan/profiles
echo "PCL cross-compiling finished!"