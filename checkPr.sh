author=$1
echo $(git blame yaml-files/createDB.py -p | grep "^author " | sort -u)
echo "$(git diff)"