cat scripts/amara_mulam.utf8 | grep \<Slok | cut -f2 -d\< | cut -f1 -d \> > scripts/sloka_indices.txt
cat scripts/sloka_indices.txt | xargs -I {} sh -c "xmlstarlet sel -t -v '//{}' -n < scripts/amara_mulam.utf8 | awk 'NF' > docker/amara/slokas/{}.utf8"

rm scripts/sloka_indices.txt
