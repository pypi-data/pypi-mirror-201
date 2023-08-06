# -*- coding: utf-8 -*-
"""
reV analysis configs (generation, lcoe, etc...)

Created on Mon Jan 28 11:43:27 2019

@author: gbuster
"""
import os
import logging
from math import ceil

from reV.config.output_request import SAMOutputRequest
from reV.config.base_analysis_config import AnalysisConfig
from reV.config.sam_config import SAMConfig
from reV.config.curtailment import Curtailment
from reV.config.project_points import PointsControl, ProjectPoints
from reV.utilities.exceptions import ConfigError
from reV.utilities import ModuleName
from reV.pipeline.pipeline import Pipeline

logger = logging.getLogger(__name__)


class SAMAnalysisConfig(AnalysisConfig):
    """SAM-based analysis config (generation, lcoe, etc...)."""
    REQUIREMENTS = ('project_points', 'sam_files', 'technology')

    def __init__(self, config):
        """
        Parameters
        ----------
        config : str | dict
            File path to config json (str), serialized json object (str),
            or dictionary with pre-extracted config.
        """
        super().__init__(config)
        self._tech = None
        self._sam_config = None
        self._pc = None
        self._default_timeout = 1800
        self._output_request = None
        self._site_data = None

    @property
    def technology(self):
        """Get the tech property from the config.

        Returns
        -------
        tech : str
            SAM technology to analyze (pvwattsv7, pvsamv1, windpower,
            tcsmoltensalt, solarwaterheat, troughphysicalheat,
            lineardirectsteam) The string is lower-cased with spaces and
            underscores removed.
        """
        if self._tech is None:
            self._tech = self['technology'].lower()
            self._tech = self._tech.replace(' ', '').replace('_', '')

        return self._tech

    @property
    def sam_files(self):
        """
        SAM config files

        Returns
        -------
        dict
        """
        return self['sam_files']

    @property
    def timeout(self):
        """Get the parallel futures timeout value in seconds.

        Returns
        -------
        timeout : int | float
            Number of seconds to wait for parallel run iteration to complete
            before returning zeros. Default is 1800 seconds.
        """
        return self.get('timeout', self._default_timeout)

    @property
    def project_points(self):
        """
        project_points input

        Returns
        -------
        pp : ProjectPoints
            ProjectPoints object
        """
        return self['project_points']

    @property
    def output_request(self):
        """Get the list of requested output variables.

        Returns
        -------
        output_request : list
            List of requested reV output variables corresponding to SAM
            variable names.
        """

        if self._output_request is None:
            self._output_request = self.get('output_request', 'cf_mean')
            self._output_request = SAMOutputRequest(self._output_request)

        return self._output_request

    @property
    def site_data(self):
        """Get the site-specific SAM inputs data file.

        Returns
        -------
        site_data : str | NoneType
            Target path for site-specific SAM inputs data file.
        """
        self._site_data = self.get('site_data', self._site_data)
        return self._site_data

    def parse_sam_config(self):
        """Get the SAM configuration object.

        Returns
        -------
        sam_gen : reV.config.sam.SAMConfig
            SAM config object. This object emulates a dictionary.
        """
        if self._sam_config is None:
            self._sam_config = SAMConfig(self['sam_files'])

        return self._sam_config

    def parse_points_control(self):
        """Get the generation points control object.

        Returns
        -------
        points_control : reV.config.project_points.PointsControl
            PointsControl object based on specified project points and
            execution control option.
        """
        if self._pc is None:
            # make an instance of project points
            pp = ProjectPoints(self.project_points, self['sam_files'],
                               tech=self.technology)

            if self.execution_control.option in ('peregrine', 'eagle'):
                # sites per split on peregrine or eagle is the number of sites
                # in project points / number of nodes. This is for the initial
                # division of the project sites between HPC nodes (jobs)
                sites_per_worker = ceil(len(pp) / self.execution_control.nodes)

            elif self.execution_control.option == 'local':
                # sites per split on local is number of sites / # of processes
                sites_per_worker = ceil(len(pp)
                                        / self.execution_control.max_workers)

            # make an instance of points control and set to protected attribute
            self._pc = PointsControl(pp, sites_per_split=sites_per_worker)

        return self._pc


class GenConfig(SAMAnalysisConfig):
    """Class to import and manage user configuration inputs."""

    NAME = ModuleName.GENERATION

    def __init__(self, config):
        """
        Parameters
        ----------
        config : str | dict
            File path to config json (str), serialized json object (str),
            or dictionary with pre-extracted config.
        """
        super().__init__(config)
        self._curtailment = None
        self._res_files = None
        self._resource_5min = None

    @property
    def curtailment(self):
        """Get the curtailment config object that the gen config points to.

        Returns
        -------
        curtailment : NoneType | reV.config.curtailment.Curtailment
            Returns None if no curtailment config is specified. If one is
            specified, this returns the reV curtailment config object.
        """
        if self._curtailment is None:
            self._curtailment = self.get('curtailment', self._curtailment)
            if self._curtailment:
                self._curtailment = Curtailment(self['curtailment'])

        return self._curtailment

    @property
    def gid_map(self):
        """Optional gid mapping that can be used to map unique generation gids
        to non-unique gids in the resource file. Should be a filepath to a csv
        with columns gid and gid_map. Can be the same csv as project_points
        input.

        Returns
        -------
        NoneType | str
        """
        return self.get('gid_map', None)

    @property
    def write_mapped_gids(self):
        """Option to write mapped gids to meta data gids instead of the gids
        from the resource data.

        Returns
        -------
        bool
        """
        return self.get('write_mapped_gids', False)

    @property
    def bias_correct(self):
        """
        Optional csv filepath to a wind or solar resource bias correction
        table. This has columns: gid, adder, scalar. If both adder and scalar
        are present, the wind or solar resource is corrected by
        (res*scalar)+adder. If either is not present, scalar defaults to 1 and
        adder to 0. Only windspeed or GHI+DNI are corrected depending on the
        technology. GHI and DNI are corrected with the same correction factors.

        Returns
        -------
        str
        """
        return self.get('bias_correct', None)

    @property
    def resource_file(self):
        """
        get base resource_file

        Returns
        -------
        str
        """
        return self['resource_file']

    @property
    def low_res_resource_file(self):
        """
        Optional low resolution resource file that will be dynamically
        mapped+interpolated to the nominal-resolution resource_file. This needs
        to be of the same format as resource_file, e.g. they both need to be
        handled by the same rex Resource handler such as WindResource

        Returns
        -------
        str
        """
        return self.get('low_res_resource_file', None)

    def _parse_res_files(self, base_res_fp):
        """Parse the base resource file input into correct ordered list format
        with year imputed in the {} format string

        Parameters
        ----------
        base_res_fp : str | list
            Base resource filepath with {} for year

        Returns
        -------
        res_fps : list
            List of resource file paths corresponding to the year list
        """

        # get base filename, may have {} for year format
        res_fps = base_res_fp
        if isinstance(res_fps, str) and '{}' in res_fps:
            # need to make list of res files for each year
            res_fps = [res_fps.format(year) for year in self.analysis_years]
        elif isinstance(res_fps, str):
            # only one resource file request, still put in list
            res_fps = [res_fps]
        elif not isinstance(res_fps, (list, tuple)):
            msg = ('Bad "resource_file" type, needed str, list, or tuple '
                   'but received: {}, {}'
                   .format(res_fps, type(res_fps)))
            logger.error(msg)
            raise ConfigError(msg)

        if len(res_fps) != len(self.analysis_years):
            msg = ('The number of resource files does not match '
                   'the number of analysis years!'
                   '\n\tResource files: \n\t\t{}'
                   '\n\tYears: \n\t\t{}'
                   .format(res_fps, self.analysis_years))
            logger.error(msg)
            raise ConfigError(msg)

        return res_fps

    def parse_res_files(self):
        """Get a list of the resource files with years filled in.

        Returns
        -------
        res_files : list
            List of config-specified resource files. Resource files with {}
            formatting will be filled with the specified year(s). This return
            value is a list with len=1 for a single year run.
        """
        if self._res_files is None:
            self._res_files = self._parse_res_files(self.resource_file)
        return self._res_files

    def parse_low_res_files(self):
        """Get a list of the resource files with years filled in.

        Returns
        -------
        low_res_files : list
            List of config-specified low-resolution resource files. Resource
            files with {} formatting will be filled with the specified year(s).
            This return value is a list with len=1 for a single year run. This
            is an optional input so might be list of None.
        """
        out = [None] * len(self.analysis_years)
        if self.low_res_resource_file is not None:
            out = self._parse_res_files(self.low_res_resource_file)
        return out


class EconConfig(SAMAnalysisConfig):
    """Class to import and manage configuration inputs for econ analysis."""

    NAME = ModuleName.ECON

    def __init__(self, config):
        """
        Parameters
        ----------
        config : str | dict
            File path to config json (str), serialized json object (str),
            or dictionary with pre-extracted config.
        """
        super().__init__(config)
        self._cf_files = None
        self._super_dirout = self.dirout
        if self.append:
            self.dirout = os.path.dirname(self.parse_cf_files()[0])

    @property
    def cf_file(self):
        """
        base cf_file path

        Returns
        -------
        str
        """
        return self['cf_file']

    @property
    def append(self):
        """Get the flag to append econ results to cf_file inputs.

        Returns
        -------
        append : bool
            Flag to append econ results to gen results. Default is False.
        """
        return bool(self.get('append', False))

    def parse_cf_files(self):
        """Get the capacity factor files (reV generation output data).

        Returns
        -------
        cf_files : list
            Target paths for capacity factor files (reV generation output
            data) for input to reV LCOE calculation.
        """

        if self._cf_files is None:
            # get base filename, may have {} for year format
            fname = self.cf_file
            if '{}' in fname:
                # need to make list of res files for each year
                self._cf_files = [fname.format(year) for
                                  year in self.analysis_years]
            elif 'PIPELINE' in fname:
                self._cf_files = Pipeline.parse_previous(
                    self._super_dirout, module=ModuleName.ECON, target='fpath'
                )
            else:
                # only one resource file request, still put in list
                self._cf_files = [fname]

            self.check_files(self._cf_files)

            # check year/cf_file matching if not a pipeline input
            if 'PIPELINE' not in fname:
                if len(self._cf_files) != len(self.analysis_years):
                    raise ConfigError('The number of cf files does not match '
                                      'the number of analysis years!'
                                      '\n\tCF files: \n\t\t{}'
                                      '\n\tYears: \n\t\t{}'
                                      .format(self._cf_files,
                                              self.analysis_years))
                for year in self.analysis_years:
                    if str(year) not in str(self._cf_files):
                        raise ConfigError('Could not find year {} in cf '
                                          'files: {}'
                                          .format(year, self._cf_files))

        return self._cf_files
