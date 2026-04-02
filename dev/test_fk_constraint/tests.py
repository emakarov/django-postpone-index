"""Module Tests"""

from config import base_tests

from django.core.management import call_command
from django.db import connections
from django.test import override_settings


class ModuleTest(base_tests.TestCase):
    __doc__ = __doc__

    module_name = __name__.split('.')[0]

    @staticmethod
    def _is_constraint_validated(db_alias, constraint_name):
        """Check if a constraint is validated via pg_constraint"""
        cursor = connections[db_alias].cursor()
        cursor.execute(
            "SELECT convalidated FROM pg_constraint WHERE conname = %s",
            [constraint_name]
        )
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None  # constraint doesn't exist
        return row[0]

    @staticmethod
    def _get_fk_constraint_name(db_alias, table_name):
        """Get FK constraint name for a table"""
        cursor = connections[db_alias].cursor()
        cursor.execute(
            "SELECT conname FROM pg_constraint "
            "WHERE conrelid = %s::regclass AND contype = 'f'",
            [table_name]
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None

    def test_004_skip_validate(self):
        """Test --skip-validate creates NOT VALID FK constraints"""
        with override_settings(
            POSTPONE_INDEX_IGNORE=True
        ):
            call_command('migrate', self.module_name, 'zero')
        with override_settings(
            POSTPONE_INDEX_IGNORE=False
        ):
            call_command('migrate', self.module_name, '0002')

            # Run with --skip-validate
            call_command('apply_postponed', 'run', '-x', '--skip-validate')

            # FK constraint should exist but NOT be validated
            constraint_name = self._get_fk_constraint_name('default', 'test_fk_constraint_fksource1')
            self.assertIsNotNone(constraint_name, 'FK constraint should exist')
            self.assertFalse(
                self._is_constraint_validated('default', constraint_name),
                'FK constraint should NOT be validated after --skip-validate'
            )

            # Now run without --skip-validate to validate
            call_command('apply_postponed', 'run', '-x')
            self.assertTrue(
                self._is_constraint_validated('default', constraint_name),
                'FK constraint should be validated after normal run'
            )

            call_command('apply_postponed', 'cleanup')
            self._assert_postponed_sql_empty()
