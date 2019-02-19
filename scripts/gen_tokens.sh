cat scripts/amara_tokens.utf8 | cut -d, -f4 | sort -u > scripts/vargas.utf8
cat scripts/vargas.utf8 | xargs -I {} sh -c 'cat scripts/amara_tokens.utf8 | grep {} > docker/amara/tokens/tokens_{}.utf8'

rm scripts/vargas.utf8
