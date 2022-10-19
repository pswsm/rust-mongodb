## Prerequisites

Make

[Docker](https://docs.docker.com/engine/install/ubuntu/)

[Docker compose](https://docs.docker.com/compose/install/)

## Environment Variables

To run this project, you will need to add the following environment variables to your production.env file

`MONGO_URI`

Example of production.env file

```bash
MONGO_URI=mongodb://EXAMPLE_USER:EXAMPLE_PASSWORD@YOUR_HOST:27017/DATABASE_NAME?authSource=admin
```

# Development environment

Start server

```bash
yarn start
```

## Deployment (docker compose)

To deploy this project run

```bash
  make deploy
```