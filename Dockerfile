FROM python:3.9-alpine

RUN mkdir -p /action

COPY ./Pipfile ./Pipfile.lock /
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY ./src /action
WORKDIR /action

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
