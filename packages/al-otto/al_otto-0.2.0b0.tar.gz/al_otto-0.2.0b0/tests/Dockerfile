FROM python

COPY requirements.txt .
COPY requirements-tests.txt .
RUN pip3 install -r ./requirements.txt
RUN pip3 install -r ./requirements-tests.txt

ENTRYPOINT [ "nox" ]

CMD [ "-f", "tests/noxfile.py" ]