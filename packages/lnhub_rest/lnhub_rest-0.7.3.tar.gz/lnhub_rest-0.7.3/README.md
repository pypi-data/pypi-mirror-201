# lnhub-rest: Cross-instance management

Note: For more extensive documentation, see [docs/content](docs/content.md).

## Summary

1. Installation
2. CLI
   1. Run server
   2. Run tests
   3. Launch Jupyter lab
   4. Migrate
3. Deployment
4. Usage
5. Release process

## 1. Installation

1. Clone this repository
2. Navigate to the repository and run:

   ```
   pip install .
   ```

## 2. CLI

To use lnhub CLI on local environment you will first have to install and configure [Supabase CLI](https://supabase.com/docs/guides/cli).

### Run server

```
lnhub run
```

### Run tests

```
lnhub test
```

### Launch Jupyter lab

```
lnhub jupyter
```

### Migrate

See [Migrations](docs/migrations.md)

## 3. Deployment

Push on the `staging` branch to deploy in staging.

Push on the `main` branch to deploy in production.

## 4. Usage

Access API documentation from these endpoints.

Locally:

```
http://localhost:8000/docs
```

On `staging` server :

```
https://lnhub-rest-cloud-run-staging-xv4y7p4gqa-uc.a.run.app/docs
```

On `production` server:

```
https://lnhub-rest-cloud-run-main-xv4y7p4gqa-uc.a.run.app/docs
```

## 5. Release process
