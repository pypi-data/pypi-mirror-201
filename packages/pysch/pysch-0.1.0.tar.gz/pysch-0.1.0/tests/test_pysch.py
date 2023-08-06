from click.testing import CliRunner
import pykeepass
from pysch import cli, common, credentials
import pytest


class TestCli():

    def test_cli_init(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['init'])
        assert result.exit_code == 0
        assert "Default configuration has been saved at" in result.output

    def test_cli_command_list(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        command_list = [
            'add-credentials',
            'connect',
            'init',
            'list-credentials',
            'list-hosts',
        ]
        assert all([command in result.output for command in command_list])

    def test_cli_connect_no_host(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['connect'])
        assert result.exit_code == 2
        assert "Missing argument 'HOST'" in result.output

    def test_cli_add_credentials(self):
        pass

    def test_cli_add_credentials_duplicate(self):
        pass

    def test_cli_delete_credentials(self):
        pass


class TestCredentialsApi():

    def test_credentials_default_file_open(self):
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        assert isinstance(cred, credentials.Credentials)
        assert isinstance(cred._kdbx, pykeepass.PyKeePass)
        assert cred._kdbx.filename == common.DEFAULT_PWDDB_FILE

    def test_credentials_add(self):
        test_entry_name = 'test_pytest'
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        entry = cred.add(
            test_entry_name,
            username='test_username',
            password='test_password'
        )
        assert isinstance(entry, pykeepass.entry.Entry)

    def test_credentials_add_duplicate(self):
        test_entry_name = 'test_pytest'
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        with pytest.raises(ValueError) as e:
            cred.add(
                test_entry_name,
                username='test_username',
                password='test_password'
            )
        assert "already exists" in str(e.value)

    def test_credentials_get(self):
        test_entry_name = 'test_pytest'
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        entry = cred.get(test_entry_name)
        assert entry is not None
        assert isinstance(entry, pykeepass.entry.Entry)
        assert entry.title == test_entry_name

    def test_credentials_get_fail(self):
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        entry = cred.get('this entry doesnt exist')
        assert entry is None

    def test_credentials_iter(self):
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        entry_list = [item for item in cred]
        all_of_entry_type = all(
            map(
                lambda ent: isinstance(ent, pykeepass.entry.Entry), entry_list
            )
        )
        assert len(entry_list) > 0
        assert all_of_entry_type is True

    def test_credentials_delete(self):
        test_entry_name = 'test_pytest'
        cred = credentials.Credentials(
            common.DEFAULT_PWDDB_FILE,
            keyfile=common.DEFAULT_PWDDB_KEY
        )
        cred.delete(test_entry_name)
