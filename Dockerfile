FROM python:3.9.2-slim-buster as pre-container

RUN mkdir /app
COPY example/django_example/setup.py /app/

# Copy over the webpack_bridge package
RUN mkdir /django-webpack-bridge
COPY webpack_bridge /django-webpack-bridge/webpack_bridge
COPY README.md /django-webpack-bridge/
COPY setup.py /django-webpack-bridge/

WORKDIR /app
RUN pip install .
COPY example/django_example /app/

FROM node:15.10.0-buster-slim as bundler

RUN mkdir /app
COPY example/webpack_example/package.json /app/

# Copy over the django_bridge package
RUN mkdir /django-webpack-bridge
COPY django_bridge /django-webpack-bridge/django_bridge
COPY package.json /django-webpack-bridge/
COPY .npmignore /django-webpack-bridge/

WORKDIR /app
RUN npm install .
COPY example/webpack_example /app/
RUN node_modules/.bin/webpack build --mode production

FROM pre-container as app-container

RUN mkdir /static
COPY --from=bundler /app/dist /static

RUN python manage.py migrate
ENTRYPOINT [ "python", "manage.py", "runserver", "0:8000" ]
