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
from pywaclient.exceptions import UnprocessableDataProvided, InternalServerException
from init_client import client

if __name__ == '__main__':
    keys = set()
    for item in client.rpg_system.list():
        if item['id'] not in [274, 267, 14, 18, 288, 287, 501, 358, 366, 372]:
            try:
                system = client.rpg_system.get(item['id'], 2)
            except UnprocessableDataProvided as err:
                print(item['id'], item['title'])
                print(err.status)
                print(err.error_summary)
                print(err.error_tracestack)
            except InternalServerException as err:
                print('Internal Server Error', item['id'], item['title'])
        else:
            print(item['title'], item['id'])
        keys.update(system.keys())
        assert item['entityClass'] == 'RPGSRD'
    print(keys)

    {'styles', 'entityClass', 'blockTemplates', 'url', 'publisher', 'author', 'campaigns', 'slug', 'subscribergroups',
     'folderId', 'state', 'blocks', 'worlds', 'description', 'success', 'icon', 'isDraft', 'heroesEnabled', 'title',
     'id', 'weight', 'updateDate', 'copyright', 'isWip', 'characters', 'reference', 'logo', 'isEditable', 'tags'}