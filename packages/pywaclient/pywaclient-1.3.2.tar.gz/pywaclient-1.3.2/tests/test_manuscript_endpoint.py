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

from init_client import world_id, client

if __name__ == '__main__':

    manuscript_1 = client.manuscript.put(
        {
            'title': 'Test Manuscript Creation',
            'world': {
                'id': world_id}

        })

    bookmark = client.manuscript.bookmark.put(
        {
            'title': 'Test Bookmark Creation',
            'manuscript': {
                'id': manuscript_1['id']
            }
        }
    )
    print(bookmark)

    print(manuscript_1)
    full_manuscript_1 = client.manuscript.get(manuscript_1['id'], 3)

    print(full_manuscript_1)
    client.manuscript.delete(manuscript_1['id'])
    client.manuscript.bookmark.delete(bookmark['id'])