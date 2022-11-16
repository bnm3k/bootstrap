#!/usr/bin/bash

set -e

_boostrap_py() {
	local dest_dir=$1
	if [[ -z $dest_dir ]]; then
		echo >&2 "Invalid arg. Is empty"
		exit 1
	fi
	if [[ ! -d $dest_dir ]]; then
		echo >&2 "Invalid dir path: '$dest_dir'"
		exit 1
	fi

	cd $dest_dir

	PYENV_VERSION=$(pyenv local)
	export PYENV_VERSION

	# git init
	echo "init git repository"
	git init

	# create python virtualenv
	echo "create virtualenv"
	test -d .venv || python3 -m venv .venv

	# activate virtualenv
	echo "activate virtualenv"
	source .venv/bin/activate

	# poetry install
	echo "install dependencies via poetry"
	poetry install

	unset PYENV_VERSION
}

_boostrap_py $1
