rm app/*.db app/*.gz
cp database/amara.db app
cp database/koshas_mulam.db app
gzip app/amara.db
gzip app/koshas_mulam.db
docker build -t aupasana/amara-quiz app
docker run -p 8888:5000 aupasana/amara-quiz
