file=static/amara_mulam.html

# line breaks at । and ॥
cp amara/amara_mulam.utf8 $file
gsed -i -e 's/।/।<br\/>/g' $file
gsed -i -e 's/॥/॥<br\/>/g' $file

# Sloka changes to divs with appropriate id
gsed -i -r 's/<Sloka_(.*)>/<div class="sloka" id="\1"><div class="sloka-number">\1<\/div>/g' $file
gsed -i -e 's/<\/Sloka_.*>/<\/div>/g' $file

# Dealing with the head and tail
gsed -i -e $'s/<doc>/<html>\\\n<body>/g' $file
gsed -i -e 's/<\/doc>/<\/body><\/html>/g' $file

sed -i -e "1r scripts/mulam_head.txt" $file

rm static/amara_mulam.html-e
