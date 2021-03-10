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
import json
from unittest.mock import patch

import json
import pytest


from ...attackers import Basic_Attacker, Even_Turn_Attacker
from ...managers.manager import Manager



@pytest.mark.api
class Test_API:
    test_threshold = -123
    test_turn = -1
    system_id = 0

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
        og_manager_connect_disconnect = deepcopy(Manager.connect_disconnect)

        def init_patch(*args, **kwargs):
            """Must be defined here to acccess client/og_init"""

            return self.init_patch(og_manager_init, client, *args, **kwargs)

        def take_action_patch(*args, **kwargs):
            return self.take_action_patch(og_manager_take_action,
                                          client,
                                          *args,
                                          **kwargs)

        def connect_disconnect_patch(*args, **kwargs):
            return self.connect_disconnect_patch(og_manager_connect_disconnect,
                                                 client,
                                                 *args,
                                                 **kwargs)

        # https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
        with patch.object(Manager, "__init__", init_patch):
            with patch.object(Manager, "take_action", take_action_patch):
                with patch.object(Manager,
                                  "connect_disconnect",
                                  connect_disconnect_patch):
                    # Don't ever import shuffle from random
                    # Or else this patch won't work
                    with patch('random.shuffle', lambda x: x):
                        with patch('random.random', lambda: 1):
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
               f'&num_buckets={len(bids)}'
               f'&manager={manager}'
               f'&sys_id={self.system_id}')

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
        url = (f'/round?bids={",".join(str(x) for x in attacked_ids)}'
               f'&sys_id={self.system_id}')
        # Compare results between api and sim
        self.compare_jsons(client.get(url).get_json()["data"],
                           manager_self.json)

    def connect_disconnect_patch(self,
                                 og_connect_disconnect,
                                 client,
                                 manager_self,
                                 user_ids_to_conn,
                                 user_cls,
                                 attacker_ids_to_conn,
                                 attacker_cls,
                                 disconnected_user_ids,
                                 test_kwarg=None):
        """Patches take_action func for manager

        calls api with the downed buckets and checks json"""

        ret_val = og_connect_disconnect(manager_self,
                              user_ids_to_conn,
                              user_cls,
                              attacker_ids_to_conn,
                              attacker_cls,
                              disconnected_user_ids)

        # Don't recurse over own args
        if test_kwarg is True:
            return
       
        url = f"/connect_disconnect?"

        conn_ids = user_ids_to_conn + attacker_ids_to_conn
        if len(conn_ids) > 0:
            url += f'cuids={",".join(str(x) for x in conn_ids)}'
        if len(disconnected_user_ids) > 0:
            if len(conn_ids) > 0:
                url += "&"
            url += f'duids={",".join(str(x) for x in disconnected_user_ids)}'

        if len(disconnected_user_ids) > 0 or len(conn_ids) > 0:
            url += "&"
        url += f'sys_id={self.system_id}'
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

        # https://stackoverflow.com/a/54565257/8903959
        assert json.loads(json.dumps(obj1),
                          parse_int=str) == json.loads(json.dumps(obj2),
                                                       parse_int=str)

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
        assert "from random iimport shuffle" not in "All source code"
        assert "from random import random" not in "all source code"
