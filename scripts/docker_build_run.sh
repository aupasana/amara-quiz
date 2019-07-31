rm app/*.db app/*.gz
cp database/amara.db app
cp database/koshas_mulam.db app
cp database/rupavali_shabda.db app
gzip app/amara.db
gzip app/koshas_mulam.db
gzip app/rupavali_shabda.db
docker build -t aupasana/amara-quiz app
docker run -p 8888:5000 aupasana/amara-quiz
