
echo add sloka to database: $1

data=`xmlstarlet sel -t -v '//Sloka_'"$1" -n < database/amara_mulam.utf8 | awk 'NF'`
sqlite3 docker/amara.db "INSERT INTO slokas VALUES ('$1', '$data')"
