import logging
from django.core.management import BaseCommand

from data import transfers
from data.models import Dataset, DataRepository, FileRecord


logging.getLogger(__name__).setLevel(logging.INFO)


def _iter_datasets(dataset_id=None, limit=None, user=None):
    dataset_ids = [dataset_id] if dataset_id is not None else transfers._incomplete_dataset_ids()
    datasets = Dataset.objects.filter(pk__in=dataset_ids).order_by('-created_datetime')
    if user is not None:
        datasets = datasets.filter(created_by__username=user)
    if limit is not None:
        datasets = datasets[:int(limit)]
    for dataset in datasets:
        yield dataset


class Command(BaseCommand):
    help = "Interact with globus"

    def add_arguments(self, parser):
        parser.add_argument('action', help='Action')
        parser.add_argument('dataset', nargs='?', help='Dataset')
        parser.add_argument('--dry', action='store_true', help='dry run')
        parser.add_argument('--data-repository', help='data repository')
        parser.add_argument('--path', help='path')
        parser.add_argument('--limit', help='limit to a maximum number of datasets')
        parser.add_argument('--user', help='select datasets created by a given user')

    def handle(self, *args, **options):
        action = options.get('action')
        dataset_id = options.get('dataset')
        path = options.get('path')
        data_repository = options.get('data_repository')
        limit = options.get('limit')
        user = options.get('user')
        dry = options.get('dry')

        if action == 'login':
            transfers.create_globus_token()
            self.stdout.write(self.style.SUCCESS("Login successful."))

        if action == 'sync':
            for dataset in _iter_datasets(dataset_id, limit=limit, user=user):
                self.stdout.write("Synchronizing file status of %s" % str(dataset))
                if not dry:
                    transfers.update_file_exists(dataset)

        if action == 'syncfast':

            # TO REMOVE after merge to master
            ibl = DataRepository.objects.get(name='IBL_cortexlab')
            ibl.globus_is_personal = False
            ibl.path = '/cortexlab/'
            ibl.save()

            zserver = DataRepository.objects.get(name='zserver')
            zserver.globus_is_personal = True
            zserver.path = '/mnt/zserver/Data/'
            zserver.globus_endpoint_id = 'f691e2ce-004a-11e8-a61e-0a448319c2f8'
            zserver.save()

            zubjects = DataRepository.objects.get(name='zubjects')
            zubjects.globus_is_personal = True
            zubjects.path = '/mnt/zubjects/'
            zubjects.globus_endpoint_id = 'f691e2ce-004a-11e8-a61e-0a448319c2f8'
            zubjects.save()

            with open(path, 'r') as f:
                existing = {p.strip(): True for p in f.readlines()}
            for fr in FileRecord.objects.filter(exists=False):
                path = transfers._get_absolute_path(fr)
                if existing.get(path, None):
                    self.stdout.write("File %s exists, updating." % path)
                    fr.exists = True
                    fr.save()

        if action == 'transfer':
            for dataset in _iter_datasets(dataset_id, limit=limit, user=user):
                to_transfer = transfers.transfers_required(dataset)
                for transfer in to_transfer:
                    self.stdout.write(
                        "Launch Globus transfer from %s:%s to %s:%s." % (
                            transfer['source_data_repository'],
                            transfer['source_path'],
                            transfer['destination_data_repository'],
                            transfer['destination_path'],
                        )
                    )
                    if not dry:
                        transfers.start_globus_transfer(
                            transfer['source_file_record'], transfer['destination_file_record'])

        if action == 'autoregister':
            if not data_repository:
                raise ValueError("Please specify a data_repository.")
            data_repository = DataRepository.objects.get(name=data_repository)
            for dir_path, filenames in transfers.iter_registered_directories(
                    data_repository=data_repository, path=path):
                print(dir_path, filenames)
