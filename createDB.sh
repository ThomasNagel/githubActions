id=0
dbContent=""
nl=$'\n'

for file in yml/*.yml; do
    newContent=`sed -e 's/^/  /' $file | sed "1 i\- id: $id"`
    ((id++))
    dbContent="$dbContent$nl$newContent"
done

echo "$dbContent" | yaml-to-sqlite metadata.db metadata /dev/stdin --pk id