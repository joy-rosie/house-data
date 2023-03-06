import pytest
import pandas


@pytest.mark.parametrize("list_df, kwargs, expected", [
    ([pandas.DataFrame()], dict(), pandas.DataFrame()),
    (
        [pandas.DataFrame(dict(a=[1, 2], b=[3, 4]))], 
        dict(), 
        pandas.DataFrame(dict(a=[1, 2], b=[3, 4])),
    ),
    # Parition column automatically gets put to the end of the dataframe 
    # and turned into a categorical
    (
        [pandas.DataFrame(dict(a=[1, 2], b=[3, 4]))], 
        dict(partition_cols=["a"]), 
        pandas.DataFrame(dict(b=[3, 4], a=pandas.Categorical([1, 2]))),
    ),
    (
        [pandas.DataFrame(dict(b=[3, 4], a=[1, 2]))],
        dict(partition_cols=["a"]), 
        pandas.DataFrame(dict(b=[3, 4], a=pandas.Categorical([1, 2]))),
    ),
    (
        [pandas.DataFrame(dict(b=[3, 4], a=pandas.Categorical([1, 2])))],
        dict(partition_cols=["a"]), 
        pandas.DataFrame(dict(b=[3, 4], a=pandas.Categorical([1, 2])))
    ),
    # Putting data in one after another works
    (
        [pandas.DataFrame(dict(a=[1], b=[3])), pandas.DataFrame(dict(a=[2], b=[4]))], 
        dict(partition_cols=["a"]), 
        pandas.DataFrame(dict(b=[3, 4], a=pandas.Categorical([1, 2]))),
    ),
    # Automatically appends data
    (
        [pandas.DataFrame(dict(a=[1], b=[3])), pandas.DataFrame(dict(a=[1], b=[4]))], 
        dict(partition_cols=["a"]), 
        pandas.DataFrame(dict(b=[3, 4], a=pandas.Categorical([1, 1]))),
    ),
    # Automatically appends data
    (
        [pandas.DataFrame(dict(a=[1], b=[2], c=[3]))], 
        dict(partition_cols=["a", "b"]), 
        pandas.DataFrame(dict(c=[3], a=pandas.Categorical([1]), b=pandas.Categorical([2]))),
    ),
    # Datetimes get converted into strings so that is not useful
    (
        [pandas.DataFrame(dict(date=[pandas.Timestamp("2020-01-01"), pandas.Timestamp("2020-01-02")], b=[1, 2]))], 
        dict(partition_cols=["date"]), 
        pandas.DataFrame(dict(
            b=[1, 2],
            date=pandas.Categorical(["2020-01-01 00:00:00.000000000", "2020-01-02 00:00:00.000000000"]),
        )),
    ),
])
def test_partition(list_df, kwargs, expected, temp_dir):
    path_serialise = temp_dir.joinpath("test.parquet")
    for df in list_df:
        df.to_parquet(path=path_serialise, **kwargs)
    actual = pandas.read_parquet(path=path_serialise)
    pandas.testing.assert_frame_equal(actual, expected)


