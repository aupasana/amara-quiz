rm *.db *.gz
cp database/amara.db app
gzip app/amara.db
docker build -t aupasana/amara-quiz app
docker run -p 8888:5000 aupasana/amara-quiz
