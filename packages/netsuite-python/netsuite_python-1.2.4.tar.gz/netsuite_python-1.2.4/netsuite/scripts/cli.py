import json
import os

import click as click
from click import prompt

from netsuite.Netsuite import Netsuite
from netsuite.settings import api_settings, IN_MEMORY_STORAGE, JSON_STORAGE
from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate, X509, X509Name, PKey, TYPE_RSA, X509Req, dump_privatekey, X509Extension)


@click.group()
def cli():
    """
    Simple CLI for managing Netsuite API Access
    """
    pass


@cli.command()
def generate_certificate():
    CN = prompt("Domain", hide_input=False)
    ORG = prompt("Organization", hide_input=False)
    ORG_UNIT = prompt("Department", hide_input=False)
    L = prompt("City", hide_input=False)
    ST = prompt("State", hide_input=False)
    C = prompt("Country", hide_input=False)
    EMAIL = prompt("Email", hide_input=False)

    NETSUITE_KEY_FILE = prompt("Netsuite Key FIle Name['./netsuite-key']: ", default=api_settings.NETSUITE_KEY_FILE)
    CERTIFICATE_FILE = './netsuite-certificate.pem'

    key = PKey()
    key.generate_key(TYPE_RSA, 4096)

    cert = X509()

    subject = cert.get_subject()
    subject.CN = CN
    subject.O = ORG
    subject.OU = ORG_UNIT
    subject.L = L
    subject.ST = ST
    subject.C = C
    subject.emailAddress = EMAIL

    cert.set_version(2)
    cert.set_issuer(subject)
    cert.set_subject(subject)
    cert.set_serial_number(int.from_bytes(os.urandom(16), byteorder="big"))
    # cert.set_serial_number(int(rand.bytes(16).encode('hex'), 16))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    with open(CERTIFICATE_FILE, 'wb+') as f:
        f.write(dump_certificate(FILETYPE_PEM, cert))
    with open(NETSUITE_KEY_FILE, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))


@cli.command()
def generate_client_config():
    client_id = prompt("What is your client id?", hide_input=False)
    cert_id = prompt("What is your Netsuite certificate id?", hide_input=False)
    cert_file = prompt("Name of Netsuite Key File['netsuite-key.pem']?", hide_input=False, default='netsuite-key.pem')

    # client_secret = prompt("What is your client secret?", hide_input=True)
    # redirect_url = prompt("Redirect URL", default=api_settings.REDIRECT_URL)
    netsuite_app_name = prompt("What is the netsuite application name?", hide_input=False)
    app_name = prompt("App Name", default=api_settings.APP_NAME)
    allow_none = prompt("Allow None", default=api_settings.ALLOW_NONE)
    use_datetime = prompt("Use Datetime", default=api_settings.USE_DATETIME)
    storage_class = prompt("Storage Class", default=api_settings.defaults.get('STORAGE_CLASS'),
                           type=click.Choice(api_settings.defaults.get('DEFAULT_STORAGE_CLASSES')),
                           show_choices=True)

    creds = {
        'CLIENT_ID': client_id,
        'NETSUITE_KEY_FILE': cert_file,
        'CERT_ID': cert_id,
        # 'CLIENT_SECRET': client_secret,
        # 'REDIRECT_URL': redirect_url,
        'NETSUITE_APP_NAME': netsuite_app_name,
        'APP_NAME': app_name,
        'ALLOW_NONE': allow_none,
        'USE_DATETIME': use_datetime,
        'STORAGE_CLASS': storage_class,
    }

    if storage_class == JSON_STORAGE:
        creds['JSON_STORAGE_PATH'] = prompt("Token Storage File", default=api_settings.JSON_STORAGE_PATH,
                                            type=click.Path(readable=True, writable=True))

    save_to_file = prompt("Save settings to file?", default='y', type=click.BOOL, show_choices=True)

    if save_to_file:
        file = prompt("Save settings to file?", default=api_settings.CREDENTIALS_PATH, type=click.File("w", ))
        file.write(json.dumps(creds, indent=4))
    else:
        click.echo(creds)

    return creds


@cli.command()
@click.option('--credentials-file', '--f', type=click.File('r'), default=api_settings.CREDENTIALS_PATH,
              prompt="Path to Credentials File")
@click.pass_context
def get_access_token(ctx, credentials_file):
    """OAuth flow for Netsuite to obtain an access and refresh token"""
    try:
        creds = json.load(credentials_file)
    except Exception as e:
        return

    creds['APP_NAME'] = prompt("What app is being used?", type=click.STRING, default=creds['APP_NAME'])

    netsuite = Netsuite(
        config=creds
    )
    netsuite.request_access_token()
    # auth_url = netsuite.get_authorization_url()
    # click.echo(f"Visit {auth_url}")
    # response_url = prompt("Paste the return url here")
    # query_string = dict(parse.parse_qsl(parse.urlsplit(response_url).query))
    # code = query_string.get('code')
    # if code:
    #     netsuite.request_access_token(code)

    if netsuite.token.access_token:
        if creds.get('STORAGE_CLASS') == IN_MEMORY_STORAGE:
            if prompt("You have chosen memory storage so nothing is saved here. Echo results?", default="y",
                      type=click.BOOL):
                click.echo(netsuite.token.__dict__)
            else:
                click.echo(f"Saved to {credentials_file}")


if __name__ == "__main__":
    cli()
