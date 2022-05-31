# Cypress testing

This run is used for manual running and writing tests.

First install cypress

```
yarn add cypress --dev
```

Run cypress in graphical mode which is useful for writing tests.

```
yarn run cypress open --env backend=http://localhost:8080,frontend=http://localhost:8081
```

Backend (http://localhost:8080) and frontend (http://localhost:8081) servers should be launched before running cypress tests.



# Dockerized run

This run used for GitHub Actions CI