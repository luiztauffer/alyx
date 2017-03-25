import os
import sys

sys.path.append(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'alyx.settings'

import django  # noqa
from django.conf import settings  # noqa

django.setup()

from subjects.models import ZygosityFinder, Subject  # noqa

zf = ZygosityFinder()

print("Updating the zygosities...")
for subject in Subject.objects.all():
    zf.genotype_from_litter(subject)
    zf.update_subject(subject)