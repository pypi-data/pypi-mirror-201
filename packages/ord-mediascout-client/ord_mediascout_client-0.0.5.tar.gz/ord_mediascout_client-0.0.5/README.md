# Mediascout ORD API client

Unofficial python client for [ORD Mediascout API](https://demo.mediascout.ru/swagger/index.html).

## Installation

    pip install ord-mediascout-client

## Usage

    from ord_mediascout_client import ORDMediascoutClient, \
        ORDMediascoutConfig, CreateClientWebApiDto, \
        ClientRelationshipType, LegalForm
    from ord_mediascout_client.client import APIError

    config = ORDMediascoutConfig(
        url='http://localhost:5000',
        username='username',
        password='password',
    )

    api = MediaScoutClient(config)

    client = Client(
        name="Test Client",
        inn="1234567890",
        ...
    )

    api = ORDMediascoutClient(config)

    client = CreateClientWebApiDto(
        createMode=ClientRelationshipType.DirectClient,
        legalForm=LegalForm.JuridicalPerson,
        inn="1234567890",
        name="Test Client",
        mobilePhone="1234567890",
        epayNumber=None,
        regNumber=None,
        oksmNumber=None
    )

    client = api.create_client(client)


## Testing

    pipenv install --dev
    pipenv shell

    # get credentials for accessing https://demo.mediascout.ru/
    # and put them into .env file (see .env.example.env)

    pytest


## Packaging

    pipenv install --dev
    pipenv shell

    vi pyproject.toml # update version

    python -m build
    python -m twine upload dist/*
