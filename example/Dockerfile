FROM python:3.9.2-slim-buster as pre-container

RUN mkdir /app
COPY django_example/setup.py /app/

WORKDIR /app
RUN pip install .
COPY django_example /app

FROM node:15.10.0-buster-slim as bundler

RUN mkdir /app
COPY webpack_example/package.json /app/

WORKDIR /app
RUN npm install .
COPY webpack_example /app
RUN webpack build --production

FROM pre-container as app-container

RUN mkdir /static
COPY --from=bundler /app/dist /static

ENTRYPOINT [ "python", "manage.py", "runserver" ]
