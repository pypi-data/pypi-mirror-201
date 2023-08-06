from project import student


def test_add_class():
    s = student.Student('test-username', 'test-uni')
    print('testing add class')
    s.add_class('test-class')
    assert s.classes == ['test-class']
    print('done')


def test_add_prof():
    s = student.Student('test-username', 'test-uni')
    print('testing add profs')
    s.add_prof('test-prof')
    assert s.profs == ['test-prof']
    print('done')


def test_remove_class():
    s = student.Student('test-username', 'test-uni')
    print('testing remove class')
    s.add_class('test-class')
    s.remove_class('test-class')
    assert s.classes == []
    print('done')


def test_remove_prof():
    s = student.Student('test-username', 'test-uni')
    print('testing remove profs')
    s.add_prof('test-prof')
    s.remove_prof('test-prof')
    assert s.profs == []
    print('done')


def test_set_uni():
    s = student.Student('test-username', 'test-uni')
    print('testing set uni')
    s.set_uni('uni-test')
    assert s.uni == 'uni-test'


def test_get_classes():
    s = student.Student('test-username', 'test-uni')
    s.add_class('test-class')
    assert s.get_classes() == ['test-class']


def test_get_profs():
    s = student.Student('test-username', 'test-uni')
    s.add_prof('test-prof')
    assert s.get_profs() == ['test-prof']


# def run_all():
#     print('running tests')
#     s = Student('test-username', 'test-uni')
#     test_set_uni(s)
#     test_add_class(s)
#     test_add_prof(s)
#     test_get_classes(s)
#     test_get_profs(s)
#     test_remove_class(s)
#     test_remove_prof(s)
