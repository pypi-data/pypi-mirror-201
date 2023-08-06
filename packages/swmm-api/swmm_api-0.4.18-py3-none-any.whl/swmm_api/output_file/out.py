__author__ = "Markus Pichler"
__credits__ = ["Markus Pichler"]
__maintainer__ = "Markus Pichler"
__email__ = "markus.pichler@tugraz.at"
__version__ = "0.1"
__license__ = "MIT"

import datetime
import warnings
from itertools import product
import numpy as np
import pandas as pd

from pandas._libs import OutOfBoundsDatetime

from .extract import SwmmOutExtract
from .definitions import OBJECTS, VARIABLES

from . import parquet_helpers as parquet
from .helpers import drop_useless_column_levels


class SwmmOutputWarning(UserWarning):
    pass


class SwmmOutput(SwmmOutExtract):
    """
    SWMM-output-file class.

    Attributes:
        filename (str): Path to the output-file (.out).
        index (pandas.DatetimeIndex): Index of the timeseries of the data.
        flow_unit (str): Flow unit. One of [``'CMS', 'LPS', 'MLD', 'CFS', 'GPM', 'MGD'``]
        labels (dict[str, list]): dictionary of the object labels as list (value) for each object type (keys are: ``'link'``, ``'node'``, ``'subcatchment'``)
        model_properties (dict[str, [dict[str, list]]]): property values for the subcatchments, nodes and links.
            The Properties for the objects are...

            - ``'subcatchment'``
                - [area]
            - ``'node'``
                - [type, invert, max. depth]
            - ``'link'``
                - type,
                - offsets
                    - ht. above start node invert (ft),
                    - ht. above end node invert (ft),
                - max. depth,
                - length

        pollutant_units (dict[str, str]): Units per pollutant.
        report_interval (datetime.timedelta): Intervall of the index.
        start_date (datetime.datetime): Start date of the data.
        swmm_version (str): SWMM Version
        variables (dict[str, list]): variables per object-type inclusive the pollutants.
        fp (file-like): Stream of the open file.
    """
    filename: str = ...
    def __init__(self, filename, skip_init=False, encoding=''):
        """
        Read a SWMM-output-file (___.out).

        Args:
            filename(str | Path): Path to the output-file (.out).
            encoding (str): Encoding of the text in the binary-file (None -> auto-detect encoding ... takes a few seconds | '' -> use default = 'utf-8')
        """
        SwmmOutExtract.__init__(self, filename, skip_init=skip_init, encoding=encoding)

        self._frame = None
        self._data = None

        if skip_init:
            return

        # the main datetime index for the results
        try:
            self.index = pd.date_range(self.start_date, periods=self.n_periods, freq=self.report_interval)
        except OutOfBoundsDatetime:
            self.index = pd.Index([self.start_date + self.report_interval * i for i in range(self.n_periods)])

    def __repr__(self):
        return f'SwmmOutput(file="{self.filename}")'

    def __enter__(self):
        return self

    def _get_dtypes(self):
        """
        Get the dtypes of the data.

        Returns:
            str: numpy types
        """
        return 'f8' + ',f4' * self.number_columns

    @property
    def number_columns(self):
        """
        Get number of columns of the full results table.

        Returns:
            int: Number of columns of the full results table.
        """
        return sum(
            len(self.variables[kind]) * len(self.labels[kind])
            for kind in OBJECTS.LIST_
        )

    @property
    def _columns_raw(self):
        """
        get the column-names of the data

        Returns:
            list[list[str]]: multi-level column-names
        """
        columns = []
        for kind in OBJECTS.LIST_:
            columns += list(product([kind], self.labels[kind], self.variables[kind]))
        return columns

    def to_numpy(self):
        """
        Convert all data to a numpy-array.

        Returns:
            numpy.ndarray: all data
        """
        if self._data is None:
            types = [('datetime', 'f8')] + [('/'.join(i), 'f4') for i in self._columns_raw]
            self.fp.seek(self._pos_start_output, 0)
            try:
                self._data = np.fromfile(self.fp, dtype=np.dtype(types))
            except:
                self._data = np.frombuffer(self.fp.read1(), dtype=np.dtype(types), count=self.n_periods)
        return self._data

    def to_frame(self):
        """
        Convert all the data to a pandas-DataFrame.

        .. Important::
            This function may take a long time if the out-file has with many objects (=columns).
            If you just want the data of a few columns use :meth:`SwmmOutput.get_part` instead.

        Returns:
            pandas.DataFrame: data
        """
        if self._frame is None:
            self._frame = self._to_pandas(self.to_numpy())
            del self._frame['datetime']
        return self._frame

    def get_part(self, kind=None, label=None, variable=None, slim=False, processes=1, show_progress=True):
        """
        Get specific columns of the data.

        .. Important::
            Set the parameter ``slim`` to ``True`` to speedup the code if you just want a few columns and
            there are a lot of objects (many columns) and just few time-steps (fewer rows) in the out-file.

        Args:
            kind (str | list): [``'subcatchment'``, ``'node'`, ``'link'``, ``'system'``] (predefined in :obj:`swmm_api.output_file.definitions.OBJECTS`)
            label (str | list): name of the objekts
            variable (str | list): variable names (predefined in :obj:`swmm_api.output_file.definitions.VARIABLES`)

                * subcatchment:
                    - ``rainfall`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.RAINFALL`
                    - ``snow_depth`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.SNOW_DEPTH`
                    - ``evaporation`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.EVAPORATION`
                    - ``infiltration`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.INFILTRATION`
                    - ``runoff`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.RUNOFF`
                    - ``groundwater_outflow`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.GW_OUTFLOW`
                    - ``groundwater_elevation`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.GW_ELEVATION`
                    - ``soil_moisture`` or :attr:`~swmm_api.output_file.definitions.SUBCATCHMENT_VARIABLES.SOIL_MOISTURE`
                * node:
                    - ``depth`` or :attr:`~swmm_api.output_file.definitions.NODE_VARIABLES.DEPTH`
                    - ``head`` or :attr:`~swmm_api.output_file.definitions.NODE_VARIABLES.HEAD`
                    - ``volume`` or :attr:`~swmm_api.output_file.definitions.NODE_VARIABLES.VOLUME`
                    - ``lateral_inflow`` or :attr:`~swmm_api.output_file.definitions.NODE_VARIABLES.LATERAL_INFLOW`
                    - ``total_inflow`` or :attr:`~swmm_api.output_file.definitions.NODE_VARIABLES.TOTAL_INFLOW`
                    - ``flooding`` or :attr:`~swmm_api.output_file.definitions.NODE_VARIABLES.FLOODING`
                * link:
                    - ``flow`` or :attr:`~swmm_api.output_file.definitions.LINK_VARIABLES.FLOW`
                    - ``depth`` or :attr:`~swmm_api.output_file.definitions.LINK_VARIABLES.DEPTH`
                    - ``velocity`` or :attr:`~swmm_api.output_file.definitions.LINK_VARIABLES.VELOCITY`
                    - ``volume`` or :attr:`~swmm_api.output_file.definitions.LINK_VARIABLES.VOLUME`
                    - ``capacity`` or :attr:`~swmm_api.output_file.definitions.LINK_VARIABLES.CAPACITY`
                * system:
                    - ``air_temperature`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.AIR_TEMPERATURE`
                    - ``rainfall`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.RAINFALL`
                    - ``snow_depth`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.SNOW_DEPTH`
                    - ``infiltration`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.INFILTRATION`
                    - ``runoff`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.RUNOFF`
                    - ``dry_weather_inflow`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.DW_INFLOW`
                    - ``groundwater_inflow`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.GW_INFLOW`
                    - ``RDII_inflow`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.RDII_INFLOW`
                    - ``direct_inflow`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.DIRECT_INFLOW`
                    - ``lateral_inflow`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.LATERAL_INFLOW`
                    - ``flooding`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.FLOODING`
                    - ``outflow`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.OUTFLOW`
                    - ``volume`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.VOLUME`
                    - ``evaporation`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.EVAPORATION`
                    - ``PET`` or :attr:`~swmm_api.output_file.definitions.SYSTEM_VARIABLES.PET`

            slim (bool): set to ``True`` to speedup the code if there are a lot of objects and just few time-steps in the out-file.
            processes (int): number of parallel processes for the slim-reading.
            show_progress (bool): show a progress bar for the slim-reading.

        Returns:
            pandas.DataFrame | pandas.Series: Filtered data.
                (return Series if only one column is selected otherwise return a DataFrame)
        """
        columns = self._filter_part_columns(kind, label, variable)
        if slim:
            values = self._get_selective_results(columns, processes=processes, show_progress=show_progress)
        else:
            values = self.to_numpy()[list(map('/'.join, columns))]

        return self._to_pandas(values, drop_useless=True)

    def _filter_part_columns(self, kind=None, label=None, variable=None):
        """
        filter which columns should be extracted

        Args:
            kind (str | list): ["subcatchment", "node", "link", "system"]
            label (str | list): name of the objekts
            variable (str | list): variable names

        Returns:
            list: filtered list of tuple(kind, label, variable)
        """

        def _filter(i, possibilities, error_label):
            if i is None:
                return possibilities
            elif isinstance(i, str):
                if i in possibilities:
                    return [i]
                else:
                    warnings.warn(f'Did not found {error_label} "{i}" in output-file, return empty data. Possibilities: {possibilities}.', SwmmOutputWarning)
                    return []
            elif isinstance(i, list):
                # return [j for j in i if j in possibilities]
                l = []
                for j in i:
                    if j in possibilities:
                        l.append(j)
                    else:
                        warnings.warn(f'Did not found {error_label} "{j}" in output-file, skipping request. Possibilities: {possibilities}', SwmmOutputWarning)
                return l

        columns = []
        for k in _filter(kind, OBJECTS.LIST_, 'object kind'):
            columns += list(product([k], _filter(label, self.labels[k], f'{k} label'), _filter(variable, self.variables[k], f'{k} variable')))
        return columns

    def _to_pandas(self, data, drop_useless=False):
        """
        convert interim results to pandas DataFrame or Series

        Args:
            data (dict, numpy.ndarray): timeseries data of swmm out file
            drop_useless (bool): if single column data should be returned as Series

        Returns:
            (pandas.DataFrame | pandas.Series): pandas Timerseries of data
        """
        if isinstance(data, dict):
            if not bool(data):
                return pd.DataFrame()
            df = pd.DataFrame.from_dict(data).set_index(self.index)
        else:
            if data.size == 0:
                return pd.DataFrame()

            if data.shape[0] != self.index.size:
                data = data[:self.index.size]

            df = pd.DataFrame(data, index=self.index, dtype=float)

        # -----------
        if df.columns.size == 1:
            return df.iloc[:, 0]
        # -----------
        df.columns = pd.MultiIndex.from_tuples([col.split('/') for col in df.columns])
        if drop_useless:
            drop_useless_column_levels(df)

        return df

    def to_parquet(self):
        """
        Write the data in a parquet file.

        multi-column-names are separated by a slash ("/")

        Uses the function :func:`swmm_api.output_file.parquet.write`, which is based on :meth:`pandas.DataFrame.to_parquet` to write the file.

        Read parquet files with :func:`swmm_api.output_file.parquet.read` to get the original column-name-structure.
        """
        parquet.write(self.to_frame(), self.filename.replace('.out', '.parquet'))

    def to_parquet_chunks(self, fn, rows_at_a_time=1000, show_progress=True, kind=None, label=None, variable=None):
        import pyarrow as pa
        import pyarrow.parquet as pq

        types = np.dtype([('datetime', 'f8')] + [('/'.join(i), 'f4') for i in self._columns_raw])
        self.fp.seek(self._pos_start_output, 0)

        parq_writer = None
        columns = self._filter_part_columns(kind, label, variable)
        use_columns = ['datetime'] + ['/'.join(c) for c in  columns]

        # ---
        if show_progress:
            import tqdm
            iterator = tqdm.trange(0, self.n_periods, rows_at_a_time)
        else:
            iterator = range(0, self.n_periods, rows_at_a_time)

        # ---
        for _ in iterator:
            # print(self.fp.tell())
            data = np.fromfile(self.fp, dtype=types, count=rows_at_a_time)[use_columns]
            df = pd.DataFrame(data)

            df.index = (pd.Timedelta(days=1) * df.pop('datetime') + self._base_date).dt.round('s')

            table = pa.Table.from_pandas(df)

            # for the first chunk of records
            if parq_writer is None:
                # create a parquet write object giving it an output file
                parq_writer = pq.ParquetWriter(fn, table.schema, compression='brotli')
            parq_writer.write_table(table)

        # close the parquet writer
        if parq_writer:
            parq_writer.close()


    # def to_netcdf(self, fn_nc):
    #     import xarray as xr
    #     df = self.to_frame()
    #     ds = df.to_xarray()
    #     ds.to_netcdf("example.nc")
    #
    #     reopened = xr.open_dataset('Example6-Final.nc')
    #
    #     print()
    #
    #     # ---------------------
    #     import netCDF4 as nc
    #     import numpy as np
    #
    #     netcdf_output = nc.Dataset(fn_nc, mode='w', format="NETCDF4")
    #
    #     # -----
    #     # Timestamps
    #     netcdf_output.createDimension(dimname='datetime', size=None)
    #     nc_time_variable = netcdf_output.createVariable(
    #         varname="datetime",
    #         datatype=datetime.datetime,
    #         dimensions=("datetime",),
    #     )
    #
    #     nc_time_variable[:] = self.index
    #
    #     nc_time_variable.units = "hours since 0001-01-01 00:00:00.0"
    #     nc_time_variable.calendar = "gregorian"
    #
    #     nc_time_variable[:] = cftime.date2num(
    #         [datetime.datetime.fromtimestamp(t) for t in swmm_output_timestamps],
    #         units=nc_time_variable.units,
    #         calendar=nc_time_variable.calendar
    #     )


read_out_file = SwmmOutput


def out2frame(filename):
    """
    Get the content of the SWMM Output file as a DataFrame

    Args:
        filename (str): filename of the output file

    Returns:
        pandas.DataFrame: Content of the SWMM Output file

    .. Important::
        Don't use this function if many object are in the out file, and you only need few of them.
        In this case use the method :meth:`SwmmOutput.get_part` instead.
    """
    out = SwmmOutput(filename)
    return out.to_frame()
