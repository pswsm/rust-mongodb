FROM python:3.8-slim-buster

RUN apt-get update -y && apt-get install --no-install-recommends -y curl bash git

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm install --location=global yarn

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

CMD yarn start