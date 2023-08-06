#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import json

from init_client import world_id, client

if __name__ == '__main__':
    premade_group_id = '92e74dbb-3ebe-4a07-999f-4e8dfb77fb33'

    group = client.subscriber_group.get(premade_group_id, 2)
    print(group)

    client.subscriber_group.patch(group['id'],
                                  {
                                      'title': 'A new title',
                                      'description': 'A different description',
                                      'position': 100,
                                      'isHidden': False,
                                      'isAssignable': False,
                                      'tags': 'anew,tag,a,day',
                                      'isDefault': False
                                  }
                                  )

    groups = client.world.subscriber_groups(world_id)
    for s in groups:
        print(json.dumps(client.subscriber_group.get(s['id'], 2), indent='    ', ensure_ascii=False))
    test_subscriber_group_1 = client.subscriber_group.put(
        {
            'title': 'Test Subscriber Group Creation',
            'world': {
                'id': world_id}
        }
    )
    test_subscriber_group_2 = client.subscriber_group.put(
        {
            'title': 'Test Subscriber Group Creation 2',
            'world': {
                'id': world_id}
        }
    )
    response_patch_subscriber_group_2 = client.subscriber_group.patch(
        test_subscriber_group_2['id'],
        {
            'title': 'A different subscriber group'
        }
    )

    full_test_subscriber_group_2 = client.subscriber_group.get(
        test_subscriber_group_2['id'],
        2
    )
    print(full_test_subscriber_group_2)

    assert full_test_subscriber_group_2['title'] == 'A different subscriber group'

    client.subscriber_group.delete(test_subscriber_group_1['id'])
    client.subscriber_group.delete(test_subscriber_group_2['id'])
