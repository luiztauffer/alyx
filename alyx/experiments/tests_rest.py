from django.contrib.auth import get_user_model
from django.urls import reverse
from alyx.base import BaseTests
from django.core.management import call_command
from actions.models import Session


class APISubjectsTests(BaseTests):

    def setUp(self):
        call_command('loaddata', 'experiments/fixtures/experiments.probemodel.json', verbosity=0)
        call_command('loaddata', 'experiments/fixtures/experiments.brainregion.json', verbosity=0)
        self.superuser = get_user_model().objects.create_superuser('test', 'test', 'test')
        self.client.login(username='test', password='test')
        self.session = Session.objects.first()
        self.session.task_protocol = 'ephys'
        self.session.save()
        self.dict_insertion = {'session': str(self.session.id),
                               'name': 'probe_00',
                               'model': '3A'}

    def test_create_list_delete_probe_insertion(self):
        # test the create endpoint
        url = reverse('probeinsertion-list')
        response = self.post(url, self.dict_insertion)
        d = self.ar(response, 201)

        # test the list endpoint
        response = self.client.get(url)
        d = self.ar(response, 200)
        # test the session filter
        urlf = url + '?&session=' + str(self.session.id) + '&name=probe_00'
        response = self.client.get(urlf)
        dd = self.ar(response, 200)
        self.assertTrue(len(dd) == 1)
        urlf = url + '?&session=' + str(self.session.id) + '&name=probe_01'
        response = self.client.get(urlf)
        dd = self.ar(response, 200)
        self.assertTrue(dd == [])

        # test the delete endpoint
        response = self.client.delete(url + '/' + d[0]['id'])
        self.ar(response, 204)

    def test_create_list_delete_trajectory(self):
        # first create a probe insertion
        insertion = {'session': str(self.session.id),
                     'name': 'probe_00',
                     'model': '3A'}
        url = reverse('probeinsertion-list')
        response = self.post(url, insertion)
        alyx_insertion = self.ar(response, 201)

        # create a trajectory
        url = reverse('trajectoryestimate-list')
        tdict = {'probe_insertion': alyx_insertion['id'],
                 'x': -4521.2,
                 'y': 2415.0,
                 'z': 0,
                 'phi': 80,
                 'theta': 10,
                 'depth': 5000,
                 'roll': 0,
                 'provenance': 'Micro-manipulator',
                 }
        response = self.post(url, tdict)
        alyx_trajectory = self.ar(response, 201)

        # test the filter/list
        urlf = (url + '?&probe_insertion=' + alyx_insertion['id'] +
                '&provenance=Micro-manipulator')
        traj = self.ar(self.client.get(urlf))
        self.assertTrue(len(traj) == 1)

        urlf = (url + '?&probe_insertion=' + alyx_insertion['id'] +
                '&provenance=Planned')
        traj = self.ar(self.client.get(urlf))
        self.assertTrue(len(traj) == 0)

        # test the delete endpoint
        response = self.client.delete(url + '/' + alyx_trajectory['id'])
        self.ar(response, 204)

    def test_create_list_delete_channels(self):
        # create the probe insertion
        pi = self.ar(self.post(reverse('probeinsertion-list'), self.dict_insertion), 201)
        tdict = {'probe_insertion': pi['id'],
                 'x': -4521.2,
                 'y': 2415.0,
                 'z': 0,
                 'phi': 80,
                 'theta': 10,
                 'depth': 5000,
                 'roll': 0,
                 'provenance': 'Micro-manipulator',
                 }
        traj = self.ar(self.post(reverse('trajectoryestimate-list'), tdict), 201)
        # post a single channel
        channel_dict = {
            'x': 111.1,
            'y': -222.2,
            'z': 333.3,
            'axial': 20,
            'lateral': 40,
            'brain_region': 1133,
            'trajectory_estimate': traj['id']
        }
        self.ar(self.post(reverse('channel-list'), channel_dict), 201)
        # post a list of channels
        chs = [channel_dict.copy(), channel_dict.copy()]
        chs[0]['axial'] = 40
        chs[1]['axial'] = 60
        response = self.post(reverse('channel-list'), chs)
        data = self.ar(response, 201)
        self.assertEqual(len(data), 2)
