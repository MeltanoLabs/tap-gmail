# `tap-gmail`

Gmail tap class.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Settings

| Setting                        | Required | Default | Description |
|:-------------------------------|:--------:|:-------:|:------------|
| oauth_credentials.client_id    | False    | None    | Your google client_id |
| oauth_credentials.client_secret| False    | None    | Your google client_secret |
| oauth_credentials.refresh_token| False    | None    | Your google refresh token |
| user_id                        | False    | me      | The user's email address. The special value me can be used to indicate the authenticated user. More info [here](https://developers.google.com/gmail/api/reference/rest/v1/users/getProfile#path-parameters) |
| messages.include_spam_trash    | False    |       0 | Include messages from SPAM and TRASH in the results. |
| stream_maps                    | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config              | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled             | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth           | False    | None    | The max depth to flatten schemas. |

A full list of supported settings and capabilities is available by running: `tap-gmail --about`


## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
poetry install
poetry run tap-gmail
```

## Configuration

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

Look at the ./generate_refresh_token.py file to generate a refresh token	


## Usage

You can easily run `tap-gmail` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-gmail --version
tap-gmail --help
tap-gmail --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_gmail/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-gmail` CLI interface directly using `poetry run`:

```bash
poetry run tap-gmail --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-gmail
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-gmail --version
# OR run a test `elt` pipeline:
meltano elt tap-gmail target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
