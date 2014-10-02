from nose.tools import assert_true

from ckan.new_tests.factories import Sysadmin
from ckan.new_tests.helpers import FunctionalTestBase, submit_and_follow

def _get_package_new_page_as_sysadmin(app):
    user = Sysadmin()
    env = {'REMOTE_USER': user['name'].encode('ascii')}
    response = app.get(
        url='/camel-photos/new',
        extra_environ=env,
    )
    return env, response


class TestDatasetFormNew(FunctionalTestBase):
    def test_dataset_form_includes_custom_fields(self):
        app = self._get_test_app()
        env, response = _get_package_new_page_as_sysadmin(app)
        form = response.forms['dataset-edit']
        assert_true('humps' in form.fields)

    def test_dataset_form_slug_says_dataset(self):
        """The default prefix shouldn't be /packages?id="""
        app = self._get_test_app()
        env, response = _get_package_new_page_as_sysadmin(app)
        form = response.forms['dataset-edit']
        assert_true('packages?id=' not in response.body)
        assert_true('/dataset/' in response.body)

    def test_resource_form_includes_custom_fields(self):
        app = self._get_test_app()
        env, response = _get_package_new_page_as_sysadmin(app)
        form = response.forms['dataset-edit']
        form['name'] = 'resource-includes-custom'

        response = submit_and_follow(app, form, env, 'save')
        form = response.forms['resource-edit']
        assert_true('camels_in_photo' in form.fields)