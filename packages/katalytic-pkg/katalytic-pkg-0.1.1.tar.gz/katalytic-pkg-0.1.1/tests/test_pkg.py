import pytest

from katalytic.pkg import _check, get_functions_in_group, get_modules, mark
from katalytic.pkg import __version__ as pkg_version


class Test_check:
    def test_all(self):
        assert _check(None, '') is False
        assert _check('load', 'save') is False
        assert _check('load', 'save::*') is False
        assert _check('save::txt', 'load::*') is False
        assert _check('load::txt', 'load::') is False

        assert _check('load::txt', 'load::txt') is True
        assert _check('load::txt', 'load::*') is True
        assert _check('load::image::png', 'load::*') is True


class Test_mark:
    def test_internals(self):
        def f1(): pass

        @mark('_test_group-1')
        def f2(): pass

        @mark('_test_group-2')
        @mark('_test_group-1')
        def f3(): pass

        assert not hasattr(f1, '__katalytic_marks__')
        assert f2.__katalytic_marks__ == ('_test_group-1', )
        assert f3.__katalytic_marks__ == ('_test_group-2', '_test_group-1')


    @pytest.mark.parametrize('group', [0, None, {}, True])
    def test_TypeError(self, group):
        with pytest.raises(TypeError):
            @mark(group)
            def f1(): pass


    @pytest.mark.parametrize('group', ['', ' ', ' \n ', '\t \t', 'no \t tabs', 'no \n newlines'])
    def test_ValueError(self, group):
        with pytest.raises(ValueError):
            @mark(group)
            def f1(): pass


class Test_get_modules:
    def test_all(self):
        modules = get_modules()
        assert 'katalytic.pkg' in [m.__name__ for m in modules]
        assert all(m.__name__.startswith('katalytic') for m in modules)


class Test_get_functions_in_group:
    def test_empty(self):
        assert get_functions_in_group('__not-used') == []
        assert get_functions_in_group('__test_3') == []

    def test_pattern(self):
        found = get_functions_in_group('__test_3*')
        found = [(name, groups) for name, _, groups in found]
        assert found == [
            ('__test', ['__test_300']),
            ('__test_2', ['__test_3::a', '__test_3::b'])
        ]

    def test_exact(self):
        found = get_functions_in_group('__test_1')
        found = [(name, groups) for name, _, groups in found]
        assert found == [('__test', ['__test_1'])]

        found = get_functions_in_group('__test_2')
        found = [(name, groups) for name, _, groups in found]
        assert found == [
            ('__test', ['__test_2']),
            ('__test_2', ['__test_2'])
        ]

class Test_version:
    def test_all(self):
        assert pkg_version is not None
