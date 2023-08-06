'''
This is a mock library for greptime, it provide same API as greptime, but it's not a real library,
you can also use it to test your scripts locally first (but mock test is still in experiment phase),
then upload them to the server for execution.
'''
from __future__ import annotations

from typing import Literal
import numpy as np
from collections import OrderedDict

import functools


def coprocessor(args=None, returns=[], sql=None, backend="rspy"):
    '''The coprocessor function accept a python script and a Record Batch:
## What it does
1. it take a python script and a [`RecordBatch`], extract columns and annotation info according to `args` given in decorator in python script
2. execute python code and return a vector or a tuple of vector,
3. the returning vector(s) is assembled into a new [`RecordBatch`] according to `returns` in python decorator and return to caller
## sql&backend
- `sql` is a string that contains SQL query, it's optional, if you provide it, execution result will be assign to `args` according to name
- `backend` is a string that contains backend name, it's optional, default to `rspy`, available backend: `rspy` and `pyo3`.
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


copr = coprocessor
i128 = i64 = i32 = i16 = i8 = int
u128 = u64 = u32 = u16 = u8 = int
f64 = f32 = float


class PyVector:
    '''This is the core class of the greptime library, it is a vector of elements, 
    in this mock library we are using numpy.ndarray to simulate it.'''

    def __init__(self, v):
        self.v: np.ndarray = v

    def from_numpy(v: np.ndarray) -> 'PyVector':
        '''Takes a numpy.ndarray and returns a PyVector object.'''
        return PyVector(v)

    def numpy(self) -> np.ndarray:
        '''Returns the numpy.ndarray object.'''
        return self.v

    def to_pyarrow(self) -> 'pyarrow.Array':
        '''Returns the pyarrow.Array object.'''
        pass

    def from_pyarrow(a: 'pyarrow.Array') -> 'PyVector':
        '''Takes a pyarrow.Array and returns a PyVector object.'''
        pass

    def __getitem__(self, key: 'int | slice') -> 'PyVector':
        '''This is a function that takes a int or slice object and returns a sliced PyVector object.
        This slice works a lot like numpy.ndarray's slice, and in local mock library it's literally a numpy.ndarray's slice.
        '''
        return PyVector(self.v[key])

    def __lt__(self, other):
        return self.v < other.v

    def __le__(self, other):
        return self.v <= other.v

    def __gt__(self, other):
        return self.v > other.v

    def __ge__(self, other):
        return self.v >= other.v

    def __eq__(self, other):
        return self.v == other.v

    def __ne__(self, other):
        return self.v != other.v

    def __add__(self, other):
        return PyVector(self.v + other.v)

    def __sub__(self, other):
        return PyVector(self.v - other.v)

    def __mul__(self, other):
        return PyVector(self.v * other.v)

    def __truediv__(self, other):
        return PyVector(self.v / other.v)

    def __floordiv__(self, other):
        return PyVector(self.v // other.v)

    def __mod__(self, other):
        return PyVector(self.v % other.v)

    def __pow__(self, other):
        return PyVector(self.v ** other.v)

    def __lshift__(self, other):
        return PyVector(self.v << other.v)

    def __rshift__(self, other):
        return PyVector(self.v >> other.v)

    def __and__(self, other):
        return PyVector(self.v & other.v)

    def __xor__(self, other):
        return PyVector(self.v ^ other.v)

    def __or__(self, other):
        return PyVector(self.v | other.v)


class PyExpr:
    def __call__(self) -> 'PyExpr':
        return self
    def alias(self, name: str) -> 'PyExpr':
        '''Return self AS name alias expression'''
        pass
    def sort(asc: bool, nulls_first: bool) -> 'PyExpr':
        '''Create a sort expression from an existing expression.'''
        pass

class PyDataFrame:
    def from_sql(sql: str) -> 'PyDataFrame':
        '''
        This is a function that takes a SQL string and 
        returns a `PyDataFrame` object constructed 
        from the result of the SQL query.
        '''
        pass

    def select_columns(self, columns: 'list[str]') -> 'PyDataFrame':
        '''Filter the `PyDataFrame` by column. Returns a new DataFrame only containing the specified columns.
        '''
        pass

    def select(self, expr_list: 'list[PyExpr]') -> 'PyDataFrame':
        '''Filter a `PyDataFrame` to only include rows that match the specified filter expression.
        '''
        pass

    def filter(self, predicate: PyExpr) -> 'PyDataFrame':
        '''Filter a `PyDataFrame` to only include rows that match the specified filter expression.'''
        pass

    def aggregate(self, group_expr: 'list[PyExpr]', aggr_expr: 'list[PyExpr]') -> 'PyDataFrame':
        '''
        Filter the `PyDataFrame` by column. Returns a new `PyDataFrame` only containing the specified columns.
        '''
        pass

    def limit(self, skip: int, fetch: int = None) -> 'PyDataFrame':
        '''
        Limit the number of rows returned from this `PyDataFrame`.

        `skip` - Number of rows to skip before fetch any row

        `fetch` - Maximum number of rows to fetch, after skipping `skip` rows.
        '''
        pass

    def union(self, df: 'PyDataFrame') -> 'PyDataFrame':
        '''
        Calculate the union of two `PyDataFrame`, 
        preserving duplicate rows.
        The two `PyDataFrame` must have exactly the same schema
        '''
        pass
    
    def union_distinct(self, df: 'PyDataFrame') -> 'PyDataFrame':
        '''
        Calculate the distinct union of two `PyDataFrame`. 
        The two `PyDataFrame` must have exactly the same schema
        '''
        pass

    def distinct(self) -> 'PyDataFrame':
        '''
        Filter out duplicate rows
        '''
        pass

    def sort(self, expr_list: 'list[PyExpr]') -> 'PyDataFrame':
        '''
        Sort the DataFrame by the specified sorting expressions. 
        Any expression can be turned into a sort expression by calling its `sort` method.
        '''
        pass

    def join(self, 
             right: 'PyDataFrame', 
             join_type: Literal["Inner", "Left", "Right", "Full", "LeftSemi", "LeftAnti", "RightSemi", "RightAnti"], 
             left_cols: 'list[str]', 
             right_cols: 'list[str]',
             filter: 'PyExpr' = None) -> 'PyDataFrame':
        '''
        Join this DataFrame with another DataFrame using the specified columns as join keys.
        Filter expression expected to contain non-equality predicates 
        that can not be pushed down to any of join inputs. 
        In case of outer join, filter applied to only matched rows.'''
        pass

    def intersect(self, df: 'PyDataFrame') -> 'PyDataFrame':
        '''
        Calculate the intersection of two DataFrames. 
        The two DataFrames must have exactly the same schema
        '''
        pass
    
    def except_df(self, df: 'PyDataFrame') -> 'PyDataFrame':
        '''
        Calculate the exception of two DataFrames. 
        The two DataFrames must have exactly the same schema
        '''
        pass

    def collect(self) -> 'PyRecordBatch':
        '''Collect the PyDataFrame into a PyRecordBatch
        ## How it work:
        Convert the logical plan represented by this DataFrame into a physical plan and execute it, 
        collecting all resulting batches into memory Executes this DataFrame and 
        collects all results into a vector of RecordBatch.
        '''
        pass

class PyRecordBatch:
    '''This is a Wrapper around a RecordBatch, 
    impl PyMapping Protocol so you can do both `a[0]` and `a["number"]` 
    to retrieve column.'''

    def __init__(self, d: OrderedDict) -> None:
        self.d = d

    def __getitem__(self, key: 'str | int') -> PyVector:
        if isinstance(key, int):
            return PyVector.from_numpy(self.d[self.d.keys()[key]])
        elif isinstance(key, str):
            return PyVector.from_numpy(self.d[key])
        else:
            raise TypeError(f'key must be int or str, but got {type(key)}')


class PyQueryEngine:
    def sql(self, sql: str) -> PyRecordBatch:
        '''This is a function that takes a SQL string and returns a PyDataFrame object.'''
        pass
    pass


def dataframe() -> PyDataFrame:
    '''This is a function that returns a PyDataFrame object, constructed from current context's input Recordbatch.'''
    pass


def query_engine() -> PyQueryEngine:
    '''This is a function that returns a PyQueryEngine object.'''
    pass


def lit(x) -> PyExpr:
    pass


def col(x: str) -> PyExpr:
    pass


def pow(x: PyVector, y: PyVector) -> PyVector:
    '''returns x^y'''
    return np.power(x.v, y.v)


def clip(x: PyVector, x_min: PyVector, x_max: PyVector) -> PyVector:
    '''This function takes a PyVector object and clip by some upper and lower bound then returns a PyVector object.'''
    return np.clip(x.v, x_min.v, x_max.v)


def diff(x: PyVector) -> list:
    '''
    an array that is different of a latter and a former element.
    TODO(discord9): this need align here
    '''
    return np.diff(x.v)


def mean(x: PyVector) -> PyVector:
    '''returns the mean of the PyVector object'''
    return np.mean(x.v)


def polyval(p: PyVector, x: PyVector) -> PyVector:
    '''
    returns the polyval of the PyVector object
    p[0]*x**(N-1) + p[1]*x**(N-2) + ... + p[N-2]*x + p[N-1]
    '''
    return np.polyval(p.v, x.v)


def argmax(x: PyVector) -> PyVector:
    '''returns the index of the maximum value of the PyVector object'''
    return np.argmax(x.v)


def argmin(x: PyVector) -> PyVector:
    '''returns the index of the minimum value of the PyVector object'''
    return np.argmin(x.v)


def percentile(x: PyVector, q: PyVector) -> PyVector:
    '''returns the q-th percentile of the PyVector object'''
    return np.percentile(x.v, q.v)


def scipy_stats_norm_cdf(x: PyVector) -> PyVector:
    '''returns the cdf of the PyVector object'''
    pass
    '''
    from scipy.stats import norm
    return norm.cdf(x.v)
    '''


def scipy_stats_norm_pdf(x: PyVector) -> PyVector:
    '''returns the pdf of the PyVector object'''
    pass
    '''
    from scipy.stats import norm
    return norm.pdf(x.v)
    '''


def sqrt(x: PyVector) -> PyVector:
    '''returns the sqrt of the PyVector object'''
    return np.sqrt(x.v)


def sin(x: PyVector) -> PyVector:
    '''returns the sin of the PyVector object'''
    return np.sin(x.v)


def cos(x: PyVector) -> PyVector:
    '''returns the cos of the PyVector object'''
    return np.cos(x.v)


def tan(x: PyVector) -> PyVector:
    '''returns the tan of the PyVector object'''
    return np.tan(x.v)


def asin(x: PyVector) -> PyVector:
    '''returns the asin of the PyVector object'''
    return np.arcsin(x.v)


def acos(x: PyVector) -> PyVector:
    '''returns the acos of the PyVector object'''
    return np.arccos(x.v)


def atan(x: PyVector) -> PyVector:
    '''returns the atan of the PyVector object'''
    return np.arctan(x.v)


def floor(x: PyVector) -> PyVector:
    '''returns the floor of the PyVector object'''
    return np.floor(x.v)


def ceil(x: PyVector) -> PyVector:
    '''returns the ceil of the PyVector object'''
    return np.ceil(x.v)


def round(x: PyVector) -> PyVector:
    '''returns the round of the PyVector object'''
    return np.round(x.v)


def trunc(x: PyVector) -> PyVector:
    '''returns the trunc of the PyVector object'''
    return np.trunc(x.v)


def abs(x: PyVector) -> PyVector:
    '''returns the abs of the PyVector object'''
    return np.abs(x.v)


def signum(x: PyVector) -> PyVector:
    '''returns the signum of the PyVector object'''
    return np.sign(x.v)


def exp(x: PyVector) -> PyVector:
    '''returns the exp of the PyVector object'''
    return np.exp(x.v)


def ln(x: PyVector) -> PyVector:
    '''returns the ln of the PyVector object'''
    return np.log(x.v)


def log2(x: PyVector) -> PyVector:
    '''returns the log2 of the PyVector object'''
    return np.log2(x.v)


def log10(x: PyVector) -> PyVector:
    '''returns the log10 of the PyVector object'''
    return np.log10(x.v)


def random(length) -> PyVector:
    '''returns a random vector of length'''
    return np.random.rand(length)


def approx_distinct(x: PyVector) -> PyVector:
    '''returns the approx_distinct of the PyVector object'''
    return np.unique(x.v).size


def median(x: PyVector) -> PyVector:
    '''returns the median of the PyVector object'''
    return np.median(x.v)


def approx_percentile_cont(x: PyVector, q: float) -> PyVector:
    '''returns the approx_percentile_cont(q-th percentile) of the PyVector object'''
    return np.percentile(x.v, q)


def array_agg(x: PyVector):
    '''returns the array_agg of the PyVector object'''
    return x.v.sum()


def avg(x: PyVector) -> PyVector:
    '''returns the avg of the PyVector object'''
    return np.mean(x.v)


def correlation(x: PyVector, y: PyVector) -> PyVector:
    '''returns the correlation of the PyVector object'''
    return np.corrcoef(x.v, y.v)[0, 1]


def count(x: PyVector) -> PyVector:
    '''returns the count of the PyVector object'''
    return x.v.size


def covariance(x: PyVector, y: PyVector) -> PyVector:
    '''returns the covariance of the PyVector object'''
    return np.cov(x.v, y.v)[0, 1]


def covariance_pop(x: PyVector, y: PyVector) -> PyVector:
    '''returns the covariance_pop of the PyVector object'''
    return np.cov(x.v, y.v, bias=True)[0, 1]


def max(x: PyVector) -> PyVector:
    '''returns the max of the PyVector object'''
    return np.max(x.v)


def min(x: PyVector) -> PyVector:
    '''returns the min of the PyVector object'''
    return np.min(x.v)


def stddev(x: PyVector) -> PyVector:
    '''returns the stddev of the PyVector object'''
    return np.std(x.v)


def stddev_pop(x: PyVector) -> PyVector:
    '''returns the stddev_pop of the PyVector object'''
    return np.std(x.v, bias=True)


def sum(x: PyVector) -> PyVector:
    '''returns the sum of the PyVector object'''
    return np.sum(x.v)


def variance(x: PyVector) -> PyVector:
    '''returns the variance of the PyVector object'''
    return np.var(x.v)


def variance_pop(x: PyVector) -> PyVector:
    '''returns the variance_pop of the PyVector object'''
    return np.var(x.v, bias=True)
