import logging

from crm.invoices import create_all_invoices


logger = logging.getLogger('cron_task')
logger.setLevel(logging.ERROR)


def generate_invoices():
    print('Generating invoices.')
    create_all_invoices()
