# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from docutils import nodes

from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx.util import logging

import otc_metadata.services

LOG = logging.getLogger(__name__)


class service_card(nodes.General, nodes.Element):
    pass


METADATA = otc_metadata.services.Services()


class ServiceCard(Directive):
    node_class = service_card
    option_spec = {
        'service_type': directives.unchanged_required,
    }

    has_content = False

    def run(self):
        node = self.node_class()
        node['service_type'] = self.options.get('service_type')
        return [node]


def service_card_html(self, node):
    # This method renders containers per each service of the category with all
    # links as individual list items
    # This method renders containers per each service of the category with all
    # links as individual list items
    data = '<div class="row row-cols-1 row-cols-md-3 g-4">'
    service = METADATA.get_service_with_docs_by_service_type(node['service_type'])
    data += (
        '<div class="col"><div class="card">'
        '<div class="card-body"><h5 class="card-title">'
        'Documents</h5></div>'
        '<ul class="list-group list-group-flush">'
    )

    for doc in service['documents']:
        if "link" not in doc:
            continue
        title = doc["title"]
        link = doc.get("link")
        data += (
            f'<li class="list-group-item"><a href="{link}">'
            f'<div class="row">'
            f'<div class="col-md-10 col-sm-10 col-xs-10">{title}</div>'
            f'</div></a></li>'
        )
    data += '</ul></div></div>'
    data += '</div>'
    self.body.append(data)
    raise nodes.SkipNode


def service_card_latex(self, node):
    # do nothing
    raise nodes.SkipNode
