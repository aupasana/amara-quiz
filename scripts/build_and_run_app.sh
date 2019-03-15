rm app/babylon.db
docker build -t aupasana/amara-quiz app
docker run -p 8888:5000 aupasana/amara-quiz
