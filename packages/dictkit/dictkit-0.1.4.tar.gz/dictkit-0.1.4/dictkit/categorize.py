import pandas as pd
from collections import namedtuple

from dictkit import UtilDict


def categorize(
    df: pd.DataFrame,
    by: str | list[str | list[str]],
    drop: bool = False,
    reset_index: bool = True,
    sort_keys: bool = False,
) -> UtilDict:
    """
    Break down a dataframe into a nested dictionary of filtered versions
    of the data.

    `fields` contains the keys to filter at each nesting level.

    If `fields="A"`, a dictionary will be returned with key/value pairs
    for each unique value in column A of `df`. The keys will be the unique values
    from column A, and values will be a filtered `df` containing only rows with that value.

    If `field=["A", "B"]`, the returned dictionary will have the same keys as above,
    but the values will instead be dictionaries with the above format, for unique values
    in column B.

    Any element in `field` can also be a list, representing a composite key to filter on.
    The function will work the same, but the dict keys for elements in this field
    will be namedtuples.

    Parameters
    ----------
    df : pandas.DataFrame
        Your data
    by : str or list[str or list[str]]
        An iterable where each element represents a nesting level. Each element can
        be either a column name, or list of column names.
    drop : bool, default False
        Whether to drop columns listed in `by`, for each resulting dataframe
    reset_index : bool, default True
        Reset the index of each resulting dataframe
    sort_keys : bool, default False
        If True, keys are placed in sorted ascending order


    Notes
    -----
    WARNING: This function is NOT efficient. Its speed will depend on how many unique values
    are in each column specified in `by`. A separate pandas filter operation will run for each
    of those values.


    Examples
    --------
    >>> df = pd.DataFrame(
    ...     zip(
    ...         ['red'] * 6 + ['gray'] * 6,
    ...         ['steak'] * 3 + ['salmon'] * 3 + ['tilapia'] * 3 + ['beef'] * 3,
    ...         pd.concat([pd.Series([x] * 2) for x in ['new york', 'vermont', 'kansas', 'florida', 'michigan', 'ohio']]),
    ...         list(range(0,12)),
    ...         [53,298,2,423,8989,3284,342,2344,2390,243,234,23],
    ...     ),
    ...     columns=['color','meat','state','ID', 'sales']
    ... )
    >>> df
       color     meat     state  ID  sales
    0    red    steak  new york   0     53
    1    red    steak  new york   1    298
    2    red    steak   vermont   2      2
    3    red   salmon   vermont   3    423
    4    red   salmon    kansas   4   8989
    5    red   salmon    kansas   5   3284
    6   gray  tilapia   florida   6    342
    7   gray  tilapia   florida   7   2344
    8   gray  tilapia  michigan   8   2390
    9   gray     beef  michigan   9    243
    10  gray     beef      ohio  10    234
    11  gray     beef      ohio  11     23

    >>> colors_dict = categorize(df, 'color')
    >>> colors_dict
    {
       'red':
            color    meat     state  ID  sales
          0   red   steak  new york   0     53
          1   red   steak  new york   1    298
          2   red   steak   vermont   2      2
          3   red  salmon   vermont   3    423
          4   red  salmon    kansas   4   8989
          5   red  salmon    kansas   5   3284,
       'gray':
            color     meat     state  ID  sales
          0  gray  tilapia   florida   6    342
          1  gray  tilapia   florida   7   2344
          2  gray  tilapia  michigan   8   2390
          3  gray     beef  michigan   9    243
          4  gray     beef      ohio  10    234
          5  gray     beef      ohio  11     23
    }

    >>> colors_dict['red']
      color    meat     state  ID  sales
    0   red   steak  new york   0     53
    1   red   steak  new york   1    298
    2   red   steak   vermont   2      2
    3   red  salmon   vermont   3    423
    4   red  salmon    kansas   4   8989
    5   red  salmon    kansas   5   3284

    >>> colors_then_meats = categorize(df, ['color', 'meat'])
    >>> colors_then_meats
    {
       'red': {
          'steak':
               color   meat     state  ID  sales
             0   red  steak  new york   0     53
             1   red  steak  new york   1    298
             2   red  steak   vermont   2      2,
          'salmon':
               color    meat    state  ID  sales
             0   red  salmon  vermont   3    423
             1   red  salmon   kansas   4   8989
             2   red  salmon   kansas   5   3284
       },
       'gray': {
          'tilapia':
               color     meat     state  ID  sales
             0  gray  tilapia   florida   6    342
             1  gray  tilapia   florida   7   2344
             2  gray  tilapia  michigan   8   2390,
          'beef':
               color  meat     state  ID  sales
             0  gray  beef  michigan   9    243
             1  gray  beef      ohio  10    234
             2  gray  beef      ohio  11     23
       }
    }
    >>> colors_then_meats['red']['salmon']
      color    meat    state  ID  sales
    0   red  salmon  vermont   3    423
    1   red  salmon   kansas   4   8989
    2   red  salmon   kansas   5   3284

    >>> state_meat_pairs = categorize(df, ['color', ['meat','state']])
    >>> gray_pairs = state_meat_pairs['gray']
    >>> gray_pairs
    {
       Key(meat='tilapia', state='florida'):
            color     meat    state  ID  sales
          0  gray  tilapia  florida   6    342
          1  gray  tilapia  florida   7   2344,
       Key(meat='tilapia', state='michigan'):
            color     meat     state  ID  sales
          0  gray  tilapia  michigan   8   2390,
       Key(meat='beef', state='michigan'):
            color  meat     state  ID  sales
          0  gray  beef  michigan   9    243,
       Key(meat='beef', state='ohio'):
            color  meat state  ID  sales
          0  gray  beef  ohio  10    234
          1  gray  beef  ohio  11     23
    }
    >>> gray_pairs['tilapia', 'michigan']
      color     meat     state  ID  sales
    0  gray  tilapia  michigan   8   2390

    >>> flat = categorize(df, [['color','meat','state']])
    >>> flat
    {
       Key(color='red', meat='steak', state='new york'):
            color   meat     state  ID  sales
          0   red  steak  new york   0     53
          1   red  steak  new york   1    298,
       Key(color='red', meat='steak', state='vermont'):
            color   meat    state  ID  sales
          0   red  steak  vermont   2      2,
       Key(color='red', meat='salmon', state='vermont'):
            color    meat    state  ID  sales
          0   red  salmon  vermont   3    423,
       Key(color='red', meat='salmon', state='kansas'):
            color    meat   state  ID  sales
          0   red  salmon  kansas   4   8989
          1   red  salmon  kansas   5   3284,
       Key(color='gray', meat='tilapia', state='florida'):
            color     meat    state  ID  sales
          0  gray  tilapia  florida   6    342
          1  gray  tilapia  florida   7   2344,
       Key(color='gray', meat='tilapia', state='michigan'):
            color     meat     state  ID  sales
          0  gray  tilapia  michigan   8   2390,
       Key(color='gray', meat='beef', state='michigan'):
            color  meat     state  ID  sales
          0  gray  beef  michigan   9    243,
       Key(color='gray', meat='beef', state='ohio'):
            color  meat state  ID  sales
          0  gray  beef  ohio  10    234
          1  gray  beef  ohio  11     23
    }

    >>> flat['gray','beef','ohio']
      color  meat state  ID  sales
    0  gray  beef  ohio  10    234
    1  gray  beef  ohio  11     23

    Those 'Key' objects are namedtuples. So we can access values
    by dot notation for better readability.
    >>> for key, data in flat.items():
    ...     print(key.color, key.meat, key.state, f'- {len(data)} rows')
    ...
    red steak new york - 2 rows
    red steak vermont - 1 rows
    red salmon vermont - 1 rows
    red salmon kansas - 2 rows
    gray tilapia florida - 2 rows
    gray tilapia michigan - 1 rows
    gray beef michigan - 1 rows
    gray beef ohio - 2 rows


    `drop` will get rid of the columns which were used as keys
    >>> categorize(df, ['color','meat'], drop=True)
    {
       'red': {
          'steak':
                   state  ID  sales
             0  new york   0     53
             1  new york   1    298
             2   vermont   2      2,
          'salmon':
                  state  ID  sales
             0  vermont   3    423
             1   kansas   4   8989
             2   kansas   5   3284
       },
       'gray': {
          'tilapia':
                   state  ID  sales
             0   florida   6    342
             1   florida   7   2344
             2  michigan   8   2390,
          'beef':
                   state  ID  sales
             0  michigan   9    243
             1      ohio  10    234
             2      ohio  11     23
       }
    }
    """

    def get_categories(df, field):
        if not isinstance(field, list):
            field = [field]

        unique_values = df[field].drop_duplicates().dropna()

        if isinstance(unique_values, pd.Series):
            unique_values = unique_values.to_frame()

        res = UtilDict()

        field_cls = namedtuple("Key", field, rename=True)

        for x in unique_values.itertuples():
            key = tuple(x)[1:]
            mapping = dict(zip(field, key))
            filtered = df
            for k, v in mapping.items():
                filtered = filtered[filtered[k] == v]
            filtered = filtered.copy()
            if reset_index:
                filtered.reset_index(drop=True, inplace=True)

            if len(key) == 1:
                res[key[0]] = filtered
            else:
                named_key = field_cls(**dict(zip(field, key)))
                res[named_key] = filtered

        if drop:
            for gdf in res.values():
                gdf.drop(columns=field, inplace=True)

        if sort_keys:
            res = UtilDict({key: res[key] for key in list(sorted(list(res.keys())))})

        return res

    df = df.copy()
    if not isinstance(by, list):
        by = [by]

    curr_field = by[0]
    by = by[1:]

    res = get_categories(df, curr_field)

    if by:
        for k, v in res.items():
            res[k] = categorize(v, by, drop, reset_index, sort_keys)

    return res


# if __name__ == "__main__":
#
#     from dictkit import UtilDict
#     df = pd.DataFrame(
#         zip(
#             ['red'] * 6 + ['gray'] * 6,
#             ['steak'] * 3 + ['salmon'] * 3 + ['tilapia'] * 3 + ['beef'] * 3,
#             pd.concat([pd.Series([x] * 2) for x in ['new york', 'vermont', 'kansas', 'florida', 'michigan', 'ohio']]),
#             list(range(0,12)),
#             [53,298,2,423,8989,3284,342,2344,2390,243,234,23],
#         ),
#         columns=['color','meat','state','ID', 'sales']
#     )
#     print(categorize(df, by=['color','meat'], drop=True))
