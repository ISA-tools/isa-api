#!/bin/bash

if [[ $TRAVIS_BRANCH == "develop" ]]; then
  git clone -b tests-dev --single-branch http://github.com/ISA-tools/ISAdatasets tests/data
else
  git clone -b tests --single-branch http://github.com/ISA-tools/ISAdatasets tests/data
fi