cat amara/amara_tokens.utf8 | cut -d, -f4 | sort -u > scripts/vargas.utf8
cat scripts/vargas.utf8 | xargs -I {} sh -c 'cat amara/amara_tokens.utf8 | grep {} > amara/tokens/tokens_{}.utf8'

cat amara/amara_mulam.utf8 | grep \<Slok | cut -f2 -d\< | cut -f1 -d \> > scripts/sloka_indices.txt
cat scripts/sloka_indices.txt | xargs -I {} sh -c "xmlstarlet sel -t -v '//{}' -n < amara/amara_mulam.utf8 | awk 'NF' > amara/slokas/{}.utf8"
