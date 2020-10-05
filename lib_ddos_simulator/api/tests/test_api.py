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


from ...attackers import Basic_Attacker, Even_Turn_Attacker
from ...managers.manager import Manager



@pytest.mark.api
class Test_API:
    test_threshold = -123
    test_turn = -1

    def test_app_running(self, client):
        """Start with a blank database."""

        rv = client.get('/')
        assert "running" in str(rv.data).lower()

    @pytest.mark.filterwarnings("ignore:Gtk")
    def test_api_json(self, client):
        """Tests the api

        I know this function is insane. This must be done this way
        so that we get access to the client through this func closure

        In short, first it patches __init__ of the manager
        in this patch, it forces the manager to call the api
        and ensure that the json is the same as it's own

        Then is patches take_action, and again checks that the
        api call is the same as it's own json

        Note that random.shuffle is patched as well
        """

        og_manager_init = deepcopy(Manager.__init__)
        og_manager_take_action = deepcopy(Manager.take_action)

        def init_patch(*args, **kwargs):
            """Must be defined here to acccess client/og_init"""

            return self.init_patch(og_manager_init, client, *args, **kwargs)

        def take_action_patch(*args, **kwargs):
            return self.take_action_patch(og_manager_take_action,
                                          client,
                                          *args,
                                          **kwargs)

        # https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
        with patch.object(Manager, "__init__", init_patch):
            with patch.object(Manager, "take_action", take_action_patch):
                # Don't ever import shuffle from random
                # Or else this patch won't work
                with patch('random.shuffle', lambda x: x):
                    # Call combo grapher, it will run sim and api in parallel
                    kwargs = {"attackers": [Basic_Attacker,
                                            Even_Turn_Attacker],
                              "num_buckets_list": [4],
                              "users_per_bucket_list": [4],
                              "num_rounds_list": [5],
                              "trials": 2}
                    # Tired of dealing with circular imports sorry
                    from ...graphers import Combination_Grapher
                    Combination_Grapher(save=True).run(**kwargs)

###############
### Patches ###
###############

    def init_patch(self,
                   og_init,
                   client,
                   manager_self,
                   num_buckets,
                   users,
                   threshold,
                   *args,
                   **kwargs):
        """Patches init func for manager

        Calls api with same init args, checks that they are the same"""

        # Unpatched init, calls init for sim
        og_init(manager_self, num_buckets, users, threshold, *args, **kwargs)
        # It's coming from our client, do not do anything else
        if threshold == Test_API.test_threshold:
            return

        # Call api with these objects
        uids, bids, manager, json_obj = self.json_to_init(manager_self.json)
        url = ("/init?"
               f'uids={",".join(str(x) for x in uids)}'
               f'&bids={",".join(str(x) for x in bids)}'
               f'&manager={manager}')

        # Check that api output and sim are the same
        self.compare_jsons(client.get(url).get_json()["data"], json_obj)

    def take_action_patch(self, og_take_action, client, manager_self, turn=0):
        """Patches take_action func for manager

        calls api with the downed buckets and checks json"""

        # Get ids
        attacked_ids = [x.id for x in manager_self.attacked_buckets]
        # Take action
        og_take_action(manager_self, turn=Test_API.test_turn)
        # Don't recurse over own args
        if turn == Test_API.test_turn:
            return
        # Call same action from api
        url = f'/turn?bids={",".join(str(x) for x in attacked_ids)}'
        # Compare results between api and sim
        self.compare_jsons(client.get(url).get_json()["data"],
                           manager_self.json)


########################
### Helper functions ###
########################

    def json_to_init(self, json_obj):
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

    def compare_jsons(self, obj1, obj2):
        """Compares manager jsons, makes sure they are correct"""

        assert obj1["manager"] == obj2["manager"]
        assert list(obj1["eliminated_users"]) == list(obj2["eliminated_users"])
        bucket_ids1 = set(str(x) for x in obj1["bucket_mapping"].keys())
        bucket_ids2 = set(str(x) for x in obj2["bucket_mapping"].keys())
        assert bucket_ids1 == bucket_ids2
        for _id in bucket_ids1:
            assert self._get_bid(obj1, _id) == self._get_bid(obj2, _id)

    def _get_bid(self, obj, _id):
        """Gets bucket id, done here for readability"""

        return_id = obj["bucket_mapping"].get(_id)
        if return_id is None:
            return_id = obj["bucket_mapping"].get(int(_id))
        return return_id

    @pytest.mark.skip(reason="No time. Iterate over all files")
    def test_random_patch(self):
        """Asserts that shuffle is never imported

        if it is it breaks the random patch and test will fail
        """

        assert False, "Not implimented"
        assert "from random import shuffle" not in "All source code"
