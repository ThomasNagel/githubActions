author=$1
echo $(git blame createDB.py -p | grep "^author " | sort -u)
echo "$(git diff)"