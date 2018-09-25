import logging
import os

import pysftp
from paramiko import RSAKey


def upload_to_sftp(file_object, filename, host, port, directory, create_sub, login, password=None, private_key=None):
    """Upload file via sftp"""
    sub_dir = ''
    protocol_error = ''
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # disable host key checking
    try:
        if password:
            logging.debug('Connecting to SSH using password')
            with pysftp.Connection(host,
                                   port=port,
                                   username=login,
                                   password=password,
                                   cnopts=cnopts) as sftp_service:
                if create_sub:
                    sub_dir = filename.split('_')[0]
                    # perhaps the subdirectory already exists from the previous uploads
                    # e.g. edition split into individual pages for Tamedia titles
                    if not sftp_service.isdir(os.path.join(directory, sub_dir)):
                        sftp_service.mkdir(sub_dir)
                sftp_service.putfo(file_object, os.path.join(directory, sub_dir, filename))
        elif private_key:

            if isinstance(private_key, RSAKey) or (isinstance(private_key, str) and os.path.exists(private_key)):
                logging.debug('Connecting to SSH using private key')
                with pysftp.Connection(host,
                                       port=port,
                                       username=login,
                                       private_key=private_key,
                                       cnopts=cnopts) as sftp_service:
                    if create_sub:
                        sub_dir = filename.split('_')[0]
                        # perhaps the subdirectory already exists from the previous uploads
                        # e.g. edition split into individual pages for Tamedia titles
                        if not sftp_service.isdir(os.path.join(directory, sub_dir)):
                            sftp_service.mkdir(sub_dir)
                    sftp_service.putfo(file_object, os.path.join(directory, sub_dir, filename))
            else:
                protocol_error = 'Private key not found'
        else:
            protocol_error = 'Missing password or private_key parameters'

    except (pysftp.ConnectionException,
            pysftp.CredentialException,
            pysftp.SSHException,
            pysftp.AuthenticationException) as e:
        logging.exception('SFTP exception')
        protocol_error = str(e) + '\n'
    except Exception as e:
        # Do not swallow any exception
        protocol_error = str(e) + '\n'
    finally:
        return protocol_error
