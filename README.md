# aws-lab_dva-c02

The way that I learn has really solidified the older I've gotten. I'm very hands on and need projects and time to explore the platform for concept. The wheels start turning and I have mini-brain-blast moments that bring everything together.

## The capstone: SimOps Board

A serverless flight-event ops board for the flight-sim/GA community (EAA 690 / VATSIM adjacent, kept as its own study project rather than a real Odyssey Aviation feature branch). Pilots check into a fly-in/VATSIM event, upload a flight log or screenshot, get tracked on a leaderboard, get notified before events start.

## Generate an .env file

```
POOL_ID=
API_ID=
USER_POOL_CLIENT_ID=
COGNITO_USERNAME=
COGNITO_PASSWORD=
AUTHORIZER_ID=
ACCOUNT_ID=
BUCKET_NAME=
VIRTUAL_ENV=
BUCKET_ARN=
UPLOAD_URL_INTEGRATION_ID=
PROCESS_UPLOAD_ARN=
TABLE_ARN=
```

## Policy / config templates

The IAM policy and Lambda config files under `policies/`
are committed as `templates/*.json.tmpl` with placeholders for account-specific values
(`${ACCOUNT_ID}`, `${BUCKET_NAME}`) instead of hardcoded values, so the real
account ID isn't published in a public repo.

Render the working `.json` files locally before using them with the AWS CLI:

```bash
npm run policies
```

This runs `scripts/render_policies.py`, which reads `templates/*.json.tmpl`,
substitutes `${VAR}` placeholders from `.env` / the environment, and writes
the result to `policies/`. The rendered `.json` files are gitignored —
re-run the command any time you pull the repo fresh or change `.env`.

## Refresh Token

```bash
export ID_TOKEN=$(aws cognito-idp initiate-auth \
    --auth-flow USER_PASSWORD_AUTH \
    --client-id $USER_POOL_CLIENT_ID \
    --auth-parameters USERNAME=$COGNITO_USERNAME,PASSWORD=$COGNITO_PASSWORD \
    --query 'AuthenticationResult.IdToken' \
    --output text)
```
