from django.test import TestCase

from ..utils import AnsibleArgumentsReference, AnsibleModules


class AnsibleTestCase(TestCase):
    def test_rules(self):
        # pylint: disable=protected-access,
        reference = AnsibleArgumentsReference()
        for rule in AnsibleArgumentsReference._GUI_TYPES_EXCEPTIONS:
            self.assertTrue(reference.is_exists(rule))

    def test_ansible_modules(self):
        mods = AnsibleModules()
        s1 = mods.get("cloud.ama*")
        s2 = mods.get("^cloud.*")
        s3 = mods.get("cloud.amazon")
        s4 = mods.all()
        s5 = mods.get(r"^(?!cloud).")
        s6 = list(set(s4) - set(s5))  # Diff between s4 and s5
        s7 = [v for v in s2 if v not in s6]  # Diff between s6 and s2
        self.assertEqual(s1, s3)
        self.assertNotEqual(s2, s1)
        self.assertEqual(len(s7), 0, s7)

        mods = AnsibleModules(detailed=True, fields="module,short_description")
        shell_module = mods.get("commands.shell")[0]
        self.assertEqual(shell_module['data']['module'], "shell", shell_module)
        self.assertEqual(shell_module['data']['short_description'],
                         "Execute commands in nodes.", shell_module)
