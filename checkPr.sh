author=$1
echo $author
echo $(git blame yaml-files/createDB.py -p | grep "^author " | sort -u)
echo "$(git diff)"