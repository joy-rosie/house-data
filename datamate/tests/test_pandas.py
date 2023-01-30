import datamate
import pandas
import pytest


DATAFRAME1 = pandas.DataFrame(dict(a=[1], b=[2]))
DATAFRAME2 = pandas.DataFrame(dict(a=[3], b=[4]))
DATAFRAME3 = pandas.DataFrame(dict(c=[3], b=[4]))
DATAFRAME4 = pandas.DataFrame(
    dict(
        a=pandas.Categorical(["a", "b", "c"]),
        b=range(3),
    )
)
DATAFRAME5 = pandas.DataFrame(
    dict(
        a=pandas.Categorical(["d", "b", "c"]),
        b=range(3, 6),
    )
)
DATAFRAME45 = pandas.DataFrame(
    dict(
        a=pandas.Categorical(["a", "b", "c", "d", "b", "c"]),
        b=range(6),
    ),
    index=[0, 1, 2, 0, 1, 2],
)
DATAFRAME45_RESET_INDEX = DATAFRAME45.reset_index(drop=True)


@pytest.mark.parametrize(
    "dfs, args, kwargs, expected",
    [
        ([pandas.DataFrame()], [], dict(), pandas.DataFrame()),
        ([DATAFRAME1], [], dict(), DATAFRAME1),
        ([DATAFRAME1, DATAFRAME1], [], dict(), pandas.concat([DATAFRAME1, DATAFRAME1])),
        ([DATAFRAME1, DATAFRAME2], [], dict(), pandas.concat([DATAFRAME1, DATAFRAME2])),
        ([DATAFRAME4], [], dict(), DATAFRAME4),
        ([DATAFRAME4, DATAFRAME5], [], dict(), DATAFRAME45),
        (
            [DATAFRAME4, DATAFRAME5],
            [],
            dict(ignore_index=True),
            DATAFRAME45_RESET_INDEX,
        ),
    ],
)
def test_concat_preserving_categorical(dfs, args, kwargs, expected):
    actual = datamate.pandas.concat_preserving_categorical(
        dfs=dfs,
        *args,
        **kwargs,
    )
    pandas.testing.assert_frame_equal(actual, expected)
