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

from bs4 import BeautifulSoup

from otc_sphinx_directives.tests import base

ref_content = (
    '<div class="row row-cols-1 row-cols-md-3 g-4" id="123456">'
    '<div class="col">'
    '<div class="card">'
    '<div class="card-body">'
    '<h5 class="card-title">Documents</h5>'
    '</div>'
    '<ul class="list-group list-group-flush">'
    '<li class="list-group-item"><a href="/elastic-cloud-server/api-ref/">'
    '<div class="row">'
    '<div class="col-md-10 col-sm-10 col-xs-10">API Reference</div>'
    '</div>'
    '</a></li>'
    '<li class="list-group-item"><a href="/elastic-cloud-server/dev-guide/">'
    '<div class="row">'
    '<div class="col-md-10 col-sm-10 col-xs-10">Developer Guide</div>'
    '</div>'
    '</a></li>'
    '<li class="list-group-item"><a href="/elastic-cloud-server/umn/">'
    '<div class="row">'
    '<div class="col-md-10 col-sm-10 col-xs-10">User Guide</div>'
    '</div>'
    '</a></li>'
    '</ul>'
    '</div>'
    '</div>'
    '</div>'
)


class TestServiceCardHTML(base.TestCase):
    """Test basic rendering.

    This can be used to test that basic rendering works for these
    examples, so if someone breaks something we know.
    """

    @base.with_app(buildername='html', srcdir=base.template_dir('service_card'))
    def setUp(self, app):
        super(TestServiceCardHTML, self).setUp()
        self.app = app
        self.app.build()
        self.html = (app.outdir / 'index.html').read_text(encoding='utf-8')
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.content = str(self.soup)

    def test_service_card(self):
        """Service Card test"""
        content = str(self.soup.find(id='123456'))
        self.assertEqual(
            ''.join(ref_content),
            content.replace('\n', '')
        )
