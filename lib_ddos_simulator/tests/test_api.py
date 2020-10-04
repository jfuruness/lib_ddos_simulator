#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This test api functionality

https://flask.palletsprojects.com/en/1.1.x/testing/
"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"
from copy import deepcopy
from unittest.mock import patch

import pytest

from ..attackers import Basic_Attacker
from ..managers.manager import Manager
from ..graphers import Combination_Grapher


@pytest.mark.api
class Test_API:
    def test_app_running(self, client):
        """Start with a blank database."""

        rv = client.get('/')
        assert "running" in str(rv.data).lower()

    @pytest.mark.filterwarnings("ignore:Gtk")
    def test_api_json(self, client):
        og_manager_init = deepcopy(Manager.__init__)

        # Must be done here to get access to client
        def init_patch(manager_self, num_buckets, users, threshold, *args, **kwargs):
            temp = og_manager_init(manager_self, num_buckets, users, threshold, *args, **kwargs)
            # It's coming from our client, do not do anything else
            if threshold == -123:
                return

    #        temp.take_action = self.take_action_patch
            uids, bids, manager, json_obj = Test_API.json_to_init_api(manager_self.json)
            data = {"manager": manager}
            assert len(uids) > 0
            data["uids"] = ",".join(str(x) for x in uids)
            assert len(bids) > 0
            data["bids"] = ",".join(str(x) for x in bids)
            url = ("/init?"
                   f'uids={",".join(str(x) for x in uids)}'
                   f'&bids={",".join(str(x) for x in bids)}'
                   f'&manager={manager}')
            resp = client.post(url)

            Test_API.compare_jsons(resp.get_json(), json_obj)

        og_manager_take_action = deepcopy(Manager.take_action)
        def take_action_patch(manager_self, turn=0):
            attacked_ids = [x.id for x in manager_self.attacked_buckets]
            og_manager_take_action(manager_self, turn=-1)
            # Don't recurse over own args
            if turn == -1:
                return
            resp = client.get('/turn?bids='+ ",".join(str(x) for x in attacked_ids))
            Test_API.compare_jsons(resp.get_json(), manager_self.json)
    
        # https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
        with patch.object(Manager, "__init__", init_patch):
            with patch.object(Manager, "take_action", take_action_patch):
                with patch("random.shuffle"):
                    combo_grapher = Combination_Grapher(save=True).run(
                                                   attackers=[Basic_Attacker],
                                                   num_buckets_list=[4],
                                                   users_per_bucket_list=[4],
                                                   num_rounds_list=[5],
                                                   trials=2)

########################
### Helper functions ###
########################

    @staticmethod        
    def json_to_init_api(json_obj):
        """Input json obj

        Output:
            url to init sim
            expected json
        """

        user_ids = []
        bucket_ids = []
        for bucket_id, user_id_list in json_obj["bucket_mapping"].items():
            user_ids.extend(user_id_list)
            bucket_ids.append(bucket_id)
        return user_ids, bucket_ids, json_obj["manager"], json_obj

    @staticmethod
    def compare_jsons(obj1, obj2):
        assert obj1["manager"] == obj2["manager"]
        assert list(obj1["eliminated_users"]) == list(obj2["eliminated_users"])
        for (bucket1, user_list1), (bucket2, user_list2) in zip(obj1["bucket_mapping"].items(),
                                                                obj2["bucket_mapping"].items()):
            assert str(bucket1) == str(bucket2)
            assert user_list1 == user_list2

