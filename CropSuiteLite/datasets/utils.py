import os
import glob

import numpy as np

import xarray
import rioxarray as rio
from rasterio.enums import Resampling


def compute_averaged_temp(
    tmin_path: str,
    tmax_path: str,
    year: int,
    suffix: str = "_v2.0.nc"
    ) -> xarray.DataArray:
    """
    Compute the daily average temperature from minimum and maximum temperatures.

    Parameters
    ----------
    tmin_path : str
        Directory path containing the minimum temperature files.
    tmax_path : str
        Directory path containing the maximum temperature files.
    year : int
        Year of the files to process.
    suffix : str, optional
        Filename suffix to match (default is "_v2.0.nc").

    Returns
    -------
    xr.DataArray
        A DataArray containing the average daily temperature for the given year,
        with dimensions (time, lat, lon).
    """
    
    tmin_file =  glob.glob(tmin_path + f'/*_{year}' + suffix)
    tmax_file = glob.glob(tmax_path + f'/*_{year}' + suffix)
        
    if not (len(tmin_file)==1 and len(tmax_file)==1):
        raise ValueError(f"No unique tmin/tmax files found for year {year}")
    
    xrdata = xarray.open_mfdataset([tmin_file[0], tmax_file[0]],  combine='nested') 
    
    tasavg = xarray.concat([xrdata["tasmax"], xrdata["tasmin"]], dim="var").mean(dim="var", skipna=True)
    tasavg.name = "tasavg"
    tasavg.attrs = xrdata.attrs
    return tasavg


class BaseProcessor():

    def __init__(self, input_pathdir: str = None) -> None:
        """
        Initialize the preprocessing class.
        """
        if input_pathdir:
            assert os.path.exists(
                input_pathdir
            ), f'The input path does not exist {input_pathdir}'

        self.input_path = input_pathdir

    @staticmethod
    def directories_list(path):
        return [
            i for i in os.listdir(path)
            if os.path.isdir(os.path.join(path, i))
        ]

    @staticmethod
    def mask_data(xrdata, mask_layer, method="bilinear"):

        if method == "bilinear":
            interp_fun = Resampling.bilinear

        elif method == "nearest":
            interp_fun = Resampling.nearest

        else:
            raise ValueError(
                f"Unsupported resampling method: {method}"
            )

        # No recortar previamente por min/max.
        # reproject_match ya calcula correctamente
        # toda la extensión de la grilla objetivo.
        xrdata_r = xrdata.rio.reproject_match(
            mask_layer,
            resampling=interp_fun
        )

        return xrdata_r.where(
            mask_layer,
            np.nan
        )

class Resample_SoilGridsData(BaseProcessor):
    """
    Utility class to handle resampling and masking of SoilGrids data.

    Parameters
    ----------
    input_pathdir : str
        Root directory containing SoilGrids GeoTIFF files organized
        by soil property variable.
    """
    def __init__(self, input_pathdir: str) -> None:
        """
        Initialize the preprocessing class.

        Parameters
        ----------
        input_pathdir : str
            Root directory containing climate model outputs.
        """
        
        super().__init__(input_pathdir)
        self._files_path_dict = None
        
    
    @property
    def files_path_dict(self):
        """
        Dictionary mapping soil variables to available GeoTIFF file paths.

        Returns
        -------
        dict of str -> list of str
            Keys are variable IDs (directory names),
            values are lists of corresponding `.tif` file paths.
        """
        if self._files_path_dict is None:
            self._files_path_dict  = {i:glob.glob(os.path.join(self.input_path, i) + f'/*.tif') for i in self.directories_list(self.input_path)}
            
        return self._files_path_dict
    
    
    
    def read_soil_property(self, variable_id: str, depth: int = None, mask_layer = None) -> xarray.DataArray:
        """
        Read a soil property layer.

        Parameters
        ----------
        variable_id : str
            Soil property identifier (e.g., 'sand', 'clay').
        depth : int, optional
            Depth index to select (default is None, meaning first file).
        mask_layer : xarray.DataArray, optional
            If provided, the layer will be masked to this extent.

        Returns
        -------
        xarray.DataArray
            Soil property raster layer as an xarray object.
        """
        fn_path = self.files_path_dict[variable_id][0] if depth is None else self.files_path_dict[variable_id][depth]
            
        soil_da = rio.open_rasterio(fn_path, masked=True).squeeze()

        if mask_layer is not None:
            soil_da = self.mask_data(soil_da, mask_layer)
            
        return soil_da
    

class NexGenPreProcessing(BaseProcessor): 
    """
    Class to preprocess CMIP6 climate data organized in a directory structure:

        variable/
            scenario/
                model/

    Example
    -------
    Directory structure:

    pr/ssp126/ACCESS-ESM1-5/
    """
    
    @property
    def variable_names(self):
        return {'tmin': 'tasmin',
         'tmax': 'tasmax',
         'prec': 'pr'}
        
    ## assumning that there is the same scenarios and models across the variables
    @property
    def variables(self):
        if self._variables is None:
            self._variables = self.directories_list(self.input_path)
        return self._variables
    
    @property
    def scenarios(self):
        if self._scenarios is None:
            self._scenarios = self.directories_list(os.path.join(self.input_path, self.variables[0]))
        return self._scenarios

    @property
    def models(self):
        if self._models is None:
            self._models = self.directories_list(os.path.join(self.input_path, self.variables[0], self.scenarios[0]))
        return self._models
    
    
    def __init__(self, input_pathdir):
        """
        Initialize the preprocessing class.

        Parameters
        ----------
        input_pathdir : str
            Root directory containing climate model outputs.
        """
        
        super().__init__(input_pathdir)
        
        self._variables = None
        self._scenarios = None
        self._models = None
        
    def create_path(self, variable, sceneratio, model):
        return os.path.join(self.input_path, variable, sceneratio, model)


    @staticmethod
    def _normalize_daily_calendar_365(xrdata, kind):
        """
        Normalize daily climate data to the 365-day annual cycle
        required by CropSuiteLite.

        Supported native calendars:
        - Gregorian/standard leap year: 366 -> remove Feb 29.
        - 365_day/noleap: preserve 365 days.
        - 360_day:
            * temperature -> interpolate annual phase 360 -> 365;
            * precipitation -> conservative cumulative remapping
              preserving annual precipitation totals.
        """

        if "time" not in xrdata.coords:
            raise RuntimeError(
                "Climate dataset has no time coordinate"
            )

        n_days = xrdata.sizes["time"]


        # ----------------------------------------------------
        # Gregorian / standard / noleap calendars
        # ----------------------------------------------------

        if n_days in (365, 366):

            is_feb29 = (
                (xrdata["time"].dt.month == 2)
                &
                (xrdata["time"].dt.day == 29)
            )

            feb29_count = int(
                is_feb29.sum()
            )

            if n_days == 366:

                if feb29_count != 1:
                    raise RuntimeError(
                        "366-day year does not contain "
                        "exactly one Feb-29"
                    )

                xrdata = xrdata.isel(
                    time=~is_feb29
                )

            elif feb29_count != 0:

                raise RuntimeError(
                    "365-day year unexpectedly contains Feb-29"
                )

            if xrdata.sizes["time"] != 365:
                raise RuntimeError(
                    "Calendar normalization did not "
                    "produce 365 days"
                )

            xrdata = xrdata.assign_coords(
                time=np.arange(
                    1,
                    366,
                    dtype=np.int16,
                )
            )

            return xrdata


        # ----------------------------------------------------
        # 360_day climate-model calendar
        # ----------------------------------------------------

        if n_days != 360:

            raise RuntimeError(
                f"Unsupported climate calendar length: "
                f"{n_days} days"
            )


        src_phase_centers = (
            np.arange(
                360,
                dtype=np.float64,
            ) + 0.5
        ) / 360.0

        dst_phase_centers = (
            np.arange(
                365,
                dtype=np.float64,
            ) + 0.5
        ) / 365.0


        # ----------------------------------------------------
        # TEMPERATURE
        #
        # Intensive variable:
        # interpolate according to relative annual position.
        # ----------------------------------------------------

        if kind == "temperature":

            original_name = getattr(
                xrdata,
                "name",
                None,
            )

            original_attrs = dict(
                xrdata.attrs
            )

            data = xrdata.assign_coords(
                _annual_phase=(
                    "time",
                    src_phase_centers,
                )
            )

            data = data.swap_dims(
                {
                    "time":
                    "_annual_phase"
                }
            )

            data = data.drop_vars(
                "time"
            )

            data = data.interp(
                _annual_phase=dst_phase_centers,
                kwargs={
                    "fill_value":
                    "extrapolate"
                },
            )

            data = data.rename(
                {
                    "_annual_phase":
                    "time"
                }
            )

            data = data.assign_coords(
                time=np.arange(
                    1,
                    366,
                    dtype=np.int16,
                )
            )

            data.attrs = original_attrs

            if original_name is not None:
                data.name = original_name

            return data


        # ----------------------------------------------------
        # PRECIPITATION
        #
        # Extensive daily quantity:
        # remap cumulative precipitation at normalized annual
        # interval edges, then difference adjacent target edges.
        #
        # This preserves annual precipitation total.
        # ----------------------------------------------------

        if kind == "precipitation":

            input_is_dataset = isinstance(
                xrdata,
                xarray.Dataset,
            )

            if input_is_dataset:

                if "pr" not in xrdata:
                    raise RuntimeError(
                        "Precipitation dataset has no "
                        "'pr' variable"
                    )

                source = xrdata["pr"]

            else:

                source = xrdata


            source_attrs = dict(
                source.attrs
            )

            dataset_attrs = (
                dict(xrdata.attrs)
                if input_is_dataset
                else None
            )


            cumulative = source.cumsum(
                dim="time"
            )

            cumulative = (
                cumulative.assign_coords(
                    _annual_edge=(
                        "time",
                        np.arange(
                            1,
                            361,
                            dtype=np.float64,
                        ) / 360.0,
                    )
                )
            )

            cumulative = cumulative.swap_dims(
                {
                    "time":
                    "_annual_edge"
                }
            )

            cumulative = cumulative.drop_vars(
                "time"
            )


            zero = xarray.zeros_like(
                source.isel(
                    time=0,
                    drop=True,
                )
            )

            zero = zero.expand_dims(
                _annual_edge=[0.0]
            )


            cumulative_edges = xarray.concat(
                [
                    zero,
                    cumulative,
                ],
                dim="_annual_edge",
            )


            target_edges = np.arange(
                366,
                dtype=np.float64,
            ) / 365.0


            cumulative_target = (
                cumulative_edges.interp(
                    _annual_edge=target_edges
                )
            )


            remapped = cumulative_target.diff(
                "_annual_edge"
            )

            remapped = remapped.rename(
                {
                    "_annual_edge":
                    "time"
                }
            )

            remapped = remapped.assign_coords(
                time=np.arange(
                    1,
                    366,
                    dtype=np.int16,
                )
            )

            remapped.attrs = source_attrs


            if input_is_dataset:

                result = remapped.to_dataset(
                    name="pr"
                )

                result.attrs = dataset_attrs

                return result


            return remapped


        raise RuntimeError(
            f"Unknown climate variable kind: {kind}"
        )


    @staticmethod    
    def _compute_mean_over_year_list(xrdata_list, year_list):
        stacked = xarray.concat(xrdata_list, dim="year")
        stacked = stacked.assign_coords(year=("year", year_list))
        
        stacked = stacked.mean(dim="year", skipna= True)
        stacked.attrs = xrdata_list[0].attrs
        
        return stacked
    
        
    def calculate_climatological_precipitation_daily_mean(
        self, starting_year: int, ending_year: int, scenario_id: str, model_id: str
    ) -> xarray.DataArray:
        """
        Calculate the climatological daily mean precipitation.

        Parameters
        ----------
        starting_year : int
            Start year.
        ending_year : int
            End year (inclusive).
        scenario_id : str
            Scenario identifier (must exist in `self.scenarios`).
        model_id : str
            Model identifier (must exist in `self.models`).

        Returns
        -------
        xr.DataArray
            Daily climatological precipitation (time=day of year).
        """
        assert scenario_id in self.scenarios
        assert model_id in self.models
        
        prec_list = []
        year_list = []
        suffix = '_v2.0.nc'
        
        for year in range(starting_year,ending_year+1):
            
            prec_path = self.create_path( self.variable_names['prec'], scenario_id, model_id)
            prec_path =  glob.glob(prec_path + f'/*_{year}' + suffix)
            
            da = xarray.open_dataset(prec_path[0])
            
            da = self._normalize_daily_calendar_365(da, kind="precipitation")
            prec_list.append(da)
            year_list.append(year)
        
        return self._compute_mean_over_year_list(prec_list, year_list)
        
    
    def calculate_climatological_temperature_daily_mean(self, starting_year, ending_year, scenario_id, model_id) -> xarray.DataArray:
        """
        Calculate the climatological daily mean temperature.

        Parameters
        ----------
        starting_year : int
            Start year.
        ending_year : int
            End year (inclusive).
        scenario_id : str
            Scenario identifier (must exist in `self.scenarios`).
        model_id : str
            Model identifier (must exist in `self.models`).

        Returns
        -------
        xarray.DataArray
            Daily climatological mean temperature (tasavg).
        """
        assert scenario_id in self.scenarios
        assert model_id in self.models
        
        xtempavg_list = []
        year_list = []
        for year in range(starting_year,ending_year+1):
            da = compute_averaged_temp(self.create_path( self.variable_names['tmin'], scenario_id, model_id), 
                            self.create_path( self.variable_names['tmax'], scenario_id, model_id), year)
            da = self._normalize_daily_calendar_365(da, kind="temperature")
            
            xtempavg_list.append(da)
            year_list.append(year)
            
        return self._compute_mean_over_year_list(xtempavg_list, year_list)
    
class NexGen(): 
    """
    Class to preprocess CMIP6 climate data organized in a directory structure:

        variable/
            scenario/
                model/

    Example
    -------
    Directory structure:

    pr/ssp126/ACCESS-ESM1-5/
    """
    @staticmethod
    def directories_list(path):
        return [i for i in os.listdir(path) if os.path.isdir(os.path.join(path, i))]

    @property
    def variable_names(self):
        return {
         'tmean': 'Temp_avg',
         'prec': 'Prec_avg'}
        
    ## assumning that there is the same scenarios and models across the variables
    @property
    def periods(self):
        if self._periods is None:
            dir_list = self.directories_list(self.input_path)
            periods_list = set()
            for i in dir_list:
                    periods_list.add('_'.join(i.split('_')[-2:]))
            self._periods = list(periods_list)

        return self._periods
    
    @property
    def scenarios(self):
        if self._scenarios is None:
            dir_list = self.directories_list(self.input_path)
            scen_list = set()
            for i in dir_list:
                    scen_list.add(i[i.index('ssp'):].split('_')[0])
            self._scenarios = list(scen_list)
        return self._scenarios

    @property
    def models(self):
        if self._models is None:
            dir_list = self.directories_list(self.input_path)
            model_list = set()
            for i in dir_list:
                    model_list.add(i.split('_')[0])
            self._models = list(model_list)

        return self._models

    def __init__(self, input_pathdir):
        """
        Initialize the preprocessing class.

        Parameters
        ----------
        input_pathdir : str
            Root directory containing climate model outputs.
        """
        
        self.input_path = input_pathdir
        self._scenarios  = None
        self._periods = None

        self._models = None