FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN prisma generate --schema /usr/src/app/data/schema.prisma

CMD [ "python", "-u", "-m", "theta"]