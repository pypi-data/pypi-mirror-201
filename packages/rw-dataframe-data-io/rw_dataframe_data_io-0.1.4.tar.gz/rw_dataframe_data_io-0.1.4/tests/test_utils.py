import pandas as pd
from utils.DataIO import file_rw


def test_file_rw_csv():
    # Test the write functionality
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    file_rw('test_csv', df, mode='write', file_extension='csv')
    # Test the read functionality
    df2 = file_rw('test_csv', mode='read', file_extension='csv',  column_name=['a', 'b'])
    print(df2)
    assert df.equals(df2)
    # assert True


def test_file_rw_pickle():
    # Test the write functionality
    obj = {'a': 1, 'b': 2}
    file_rw('test_pickle', obj, mode='write', file_extension='pkl')
    # Test the read functionality
    obj2 = file_rw('test_pickle', mode='read', file_extension='pkl')
    assert obj == obj2


def test_file_rw_json():
    # Test the write functionality
    obj = {'a': 1, 'b': 2}
    file_rw('test_json', obj, mode='write', file_extension='json')
    # Test the read functionality
    obj2 = file_rw('test_json', mode='read', file_extension='json')
    assert obj == obj2