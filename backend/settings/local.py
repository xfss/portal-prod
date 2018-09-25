from settings.base import *

SECRET_KEY = '=hu8#4d+)g-@o1i+9qa6zf**+r-!ledo!rg5wii!!c8vt9a!3v'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

CRONJOBS = [
    ('0 4 * * */1', 'status.cron_tasks.check_edition_schedules'),
    ('0 4 1 * *', 'crm.cron_tasks.generate_invoices')
]
