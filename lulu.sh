#!/bin/bash

##############################
# install script for MacOS
# Written from Kevin
# For The Best Girl Lulu :D
##############################

##############################
# vim主題顏色設定
# ref 
# 1.https://zhung.com.tw/article/%E8%A8%AD%E5%AE%9Avimrc%E8%AE%93mac%E5%85%A7%E5%BB%BA%E7%9A%84vim%E6%9B%B4%E7%BE%8E%E8%A7%80%E5%A5%BD%E7%94%A8/
# 2.https://clay-atlas.com/blog/2020/05/04/vim-cn-note-scheme-colors-settings/
echo "創建colors資料夾"
cd mkdir ~/.vim/colors
touch ~/.vimrc

git clone https://github.com/vim-scripts/Risto-Color-Scheme.git
cp Risto-Color-Scheme/colors/risto.vim ~/.vim/colors/

##############################

# brew install kubectl  安裝k8s
# brew install minikube 安裝k8s叢集
# brew install iterm 安裝i終端機

##### ref #####
echo "This is ref --> https://medium.com/nitas-learning-journey/mac%E7%B5%82%E7%AB%AF%E6%A9%9F-terminal-%E8%A8%AD%E5%AE%9A-iterm2-ba63efd0df6a"
###############

# 安裝homebrew
# /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# 顏色文字
# printf "\E[1;32;40m"
# echo "Check Install SUCCESS"
# printf "0m"
# 顏色文字
# sleep 0.5s
# brew --version
# brew cask install iterm2 安裝iterm2

# brew oh-myzsh 

