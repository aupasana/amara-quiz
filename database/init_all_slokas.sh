
cat database/amara_mulam.utf8 | grep \<Slok | cut -f2 -d\< | cut -f1 -d \> | cut -d_ -f2 > database/tmp_sloka_indicies.txt

cat database/tmp_sloka_indicies.txt | xargs -I {} sh -c "database/init_single_sloka.sh {}"

rm database/tmp_sloka_indicies.txt
