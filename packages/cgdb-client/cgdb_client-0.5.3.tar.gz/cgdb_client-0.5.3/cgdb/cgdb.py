from typing import List

from cgdb.managers import AggregationsManager
from cgdb.managers import ElementsManager
from cgdb.managers import FlagListManager
from cgdb.managers import SitesManager
from cgdb.managers import DataSetsManager
from cgdb.managers import StationNetworksManager
from cgdb.managers import TimeStepsManager
from cgdb.resources import Site
from cgdb.resources import StationGroup
from cgdb.resources import Element
from cgdb.resources import Aggregation
from cgdb.resources import ElementContext
from cgdb.resources import TimeStep
from cgdb.managers import DepartmentsManager
from cgdb.managers import ElementsCategoriesManager
from cgdb.managers import ParametersManager
from cgdb.managers import ElementContextsManager
from cgdb.managers import StationGroupsManager
from cgdb.managers import LevelsManager

from cgdb.utils import CGDBAPISession
import cgdb.config
import urllib3
urllib3.disable_warnings()

class CGDB:
    """Client class for communication with CGDB
    """
    def __init__(self, api_key, host=None, debug_post=False, debug_get=False):
        """ :type api_key: str
            :param api_key: api key for authenticate to api endpoint

            :type host: str or None
            :param host: api endpoint url
        """
        if host is None:
            host = "https://gari.local.czechglobe.cz:8443/api/"
        self._session = CGDBAPISession(host, api_key)
        self._sites_manager = SitesManager(client=self)
        self._data_sets_manager = DataSetsManager(client=self)
        self._departments_manager = DepartmentsManager(client=self)
        self._elements_manager = ElementsManager(client=self)
        self._elements_categories_manager = ElementsCategoriesManager(client=self)
        self._flag_lists_manager = FlagListManager(client=self)
        self._parameters_manager = ParametersManager(client=self)
        self._time_steps_manager = TimeStepsManager(client=self)
        self._element_contexts_manager = ElementContextsManager(client=self)
        self._station_networks_manager = StationNetworksManager(client=self)
        self._aggregations_manager = AggregationsManager()
        self._station_groups_manager = StationGroupsManager(client=self)
        self._levels_manager = LevelsManager(client=self)
        cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB_GET = debug_get
        cgdb.config.DEBUG_CONSOLE_LOG_CGDB_LIB_POST = debug_post


    def sites(self):
        """Get all sites/stations
        """
        return self._sites_manager.sites()

    def site(self, code) -> Site:
        """Get site/station by mark

            :type code: str
            :param code: code of site/station
        """
        return self._sites_manager.site(code)

    def station_groups(self):
        """Get all sites groups
        """
        return self._station_groups_manager.station_groups()

    def station_group(self, code) -> StationGroup:
        """Get station group by code

            :type code: str
            :param code: code of site/station
        """
        return self._station_groups_manager.station_group(code)

    def departments(self):
        """Get all depatments groups
        """
        return self._departments_manager.departments()

    def department(self, id: str):
        """Get depatment by code

            :type code: str
            :param code: code of site/station
        """
        return self._departments_manager.department(id)

    def levels(self):
        return self._levels_manager.levels()
    
    def level(self, code):
        return self._levels_manager.level_by_code(code)

    def elements(self):
        """Get all elements groups
        """
        return self._elements_manager.elements()

    def element(self, mark: str) -> Element:
        """Get element by code

            :type code: str
            :param code: code of site/station
        """
        return self._elements_manager.element(mark)

    def element_contexts(self) -> ElementContext:
        """Get all elements contexts
        """
        return self._element_contexts_manager.element_contexts()

    def element_context_by_element(self, element_mark: str, aggregation: str, timestamp_code: str, level_code:str = None):
        return self._element_contexts_manager.element_context_by_element(element_mark, aggregation, timestamp_code, level_code)
    def create_element_context(self, element, aggregation, timeStep, level=None):
        return self._element_contexts_manager.create_element_context(element, aggregation, timeStep, level)

    def time_steps(self):
        """Get all time steps
        """
        return self._time_steps_manager.time_steps()

    def time_step(self, code) -> TimeStep:
        """Get time step by code

            :type code: str
            :param code: code of site/station
        """
        return self._time_steps_manager.time_step_by_code(code)

    def aggregations(self) -> List[Aggregation]:
        """Get aggregation by code

            :type code: str
            :param code: code of site/station
        """
        return self._aggregations_manager.aggregations()

    def create_data_set(self, site, element_code, aggregation_code, time_step_code, data_set_type, elementMarkOverride= None, level_code=None, description=None):
        """Create data set

             :type site: Site
             :param site: object of site

             :type element_code: str
             :param element_code: code of element

             :type aggregation_code: str
             :param aggregation_code: code of aggregation

             :type time_step_code: str
             :param time_step_code: code of time_step

             :type description: str
             :param description: code of description
         """
        if self.element_context_by_element(
                element_code,
                aggregation_code,
                time_step_code,
                level_code) is None:
            if level_code is not None:
                self.create_element_context(self.element(element_code), aggregation_code, self.time_step(time_step_code),
                                                   self.level(level_code))
            else:
                self.create_element_context(self.element(element_code), aggregation_code,
                                            self.time_step(time_step_code))
        self._data_sets_manager.create_data_set(site, element_code, aggregation_code, time_step_code, level_code, data_set_type, elementMarkOverride, description=description)

    def create_station(self, name: str, code: str, gpsLatitude: float, gpsLongitude: float, altitude: int, stationNetworkCode:str, stationGroupCode:str = None, remark=""):
        """Create station

             :type name: str
             :param name: name of station

             :type code: str
             :param code: code of station

             :type gpsLatitude: float
             :param gpsLatitude: gps latitude

             :type gpsLongitude: float
             :param gpsLongitude: gps longitude

             :type altitude: int
            :param altitude: altitude

            :type stationNetworkCode: str
            :param stationNetworkCode: code of station network that station is member of
         """
        self._sites_manager.create_station(name, code, gpsLatitude, gpsLongitude, altitude, stationNetworkCode, stationGroupCode, remark)

    def create_station_group(self, code, name=None, description=None):
        """Create station

         :type name: str
         :param name: name of station group

         :type code: str
         :param code: code of station group

         :type description: str
         :param description: description of station group
        """
        self._station_groups_manager.create_station_group(code, name, description)

    