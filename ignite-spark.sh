#!/bin/bash

DEFAULT_EMAIL="massimo.mund@lancode.de"
DEFAULT_AUTHOR="Massimo Mund"
DEFAULT_PROJECT_NAME="spark"
DEFAULT_PYTHON_VERSION="3.5"
DEFAULT_GIT_REPO="https://github.com/masmu/spark"

function replace_text () {
    find ./ -type f \
             -not -path "./.git/*" \
             -not -path "./prepare-spark.sh" \
             -exec sed -i -e "s!$1!$2!g" {} \;
}

function replace_python_version() {
    replace_text "py${1:0:1}${1:2}" "py${2:0:1}${2:2}"
    replace_text "Python ${1}" "Python ${2}"
    replace_text "python${1}" "python${2}"
    replace_text "python: ${1}" "python: ${2}"
    replace_text "Python :: ${1}" "Python :: ${2}"
}

function rename_files() {
    find "$1" -type f -name "*$2*" | while read FILE ; do
        NEW_FILE="$(echo ${FILE} | sed "s/$2/$3/")"
        mv "${FILE}" "${NEW_FILE}"
    done 
}

cd "$(dirname "$0")"
if [ ! -d "./$DEFAULT_PROJECT_NAME" ]; then
    echo "Could not find ./$DEFAULT_PROJECT_NAME! Project already renamed?"
    exit 1
fi

while [ "$#" -gt "0" ]; do
    case $1 in
    --email|-e)
        EMAIL="$2"
        shift 2
    ;;
    --author|-a)
        AUTHOR="$2"
        shift 2
    ;;
    --git-repo|-g)
        GIT_REPO="$2"
        shift 2
    ;;
    --python|-p)
        PYTHON_VERSION="$2"
        shift 2
    ;;
    --empty-git)
        shift
        EMPTY_GIT="1"
    ;;
    *)
        PROJECT_NAME="$1"
        shift 1
    ;;
    esac
done

if [ "$PROJECT_NAME" == "" ]; then
    echo 'You have to specify an project name using the --name option.'
    exit 1
fi
if [ "$GIT_REPO" == "" ]; then
    echo 'You have to specify a git repo using the --git-repo option.'
    exit 1
fi
rm "$0"

echo "Project name: $PROJECT_NAME"
replace_text "$DEFAULT_PROJECT_NAME" "$PROJECT_NAME"

echo "Git: $GIT_REPO"
replace_text "$DEFAULT_GIT_REPO" "$GIT_REPO"

if [ "$EMAIL" != "" ]; then
    echo "Email: $EMAIL"
    replace_text "$DEFAULT_EMAIL" "$EMAIL"
fi

if [ "$AUTHOR" != "" ]; then
    echo "Author: $AUTHOR"
    replace_text "$DEFAULT_AUTHOR" "$AUTHOR"
fi

if [ "$PYTHON_VERSION" != "" ]; then
    echo "Python: $PYTHON_VERSION"
    replace_python_version "$DEFAULT_PYTHON_VERSION" "$PYTHON_VERSION"
fi


[[ -d ./debian ]] && rename_files ./debian "$DEFAULT_PROJECT_NAME" "$PROJECT_NAME"
[[ -d ./contrib ]] && rename_files ./contrib "$DEFAULT_PROJECT_NAME" "$PROJECT_NAME"
[[ -d ./$DEFAULT_PROJECT_NAME ]] && mv ./"$DEFAULT_PROJECT_NAME" ./"$PROJECT_NAME"

if [[ "$EMPTY_GIT" == "1" ]] ; then
    [[ -d ./.git/ ]] && rm -rf ./.git/
    git init
    git add *
    git add .coveragerc .travis.yml .gitignore
    git commit -am "Initial commit"
    git remote add origin "${GIT_REPO}"
fi

echo "Done."
