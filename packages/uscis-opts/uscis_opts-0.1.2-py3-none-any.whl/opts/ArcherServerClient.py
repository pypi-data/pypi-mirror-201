import datetime
import re
import warnings
import xml.etree.ElementTree as ET
import pandas as pd

from opts.ContextError import ContextError

try:
  import importlib.resources as pkg_resources
except ImportError:
  # Try backported to PY<37 'importlib_resources'.
  import importlib_resources as pkg_resources

# Relative Imports
from . import templates

class ArcherServerClient:
  """
  ArcherAPI.ArcherServerClient

  A wrapper class to simplify Archer API calls. The different Archer APIs do NOT
  have feature parity. You will see calls to different Archer APIs in this
  class.

  Methods that a user interacts with currently return the following types:
  -- str
  -- pandas.DataFrame

  Types to avoid returning:
  -- xml.etree.* (I personally do not find xml or this module intuitive.
                  Please feel free to improve the code in this class.)

  Available Archer APIs:
  1) Web Services
  2) RESTful
  3) Content

  See the Archer documentaion for more information.
  """
  
  def get_report_guid(self, name: str) -> str:
    """
    Get GUID of report. Used in future API queries, specifically to generate
    search options for Execute Search.

    API Used: Web Services

    Positional arguments:
    name -- Name of report.
    """

    url = f'{self.auth.base_url}/ws/search.asmx'

    # Request data stored in templates.
    data = ET.parse(pkg_resources.open_text(templates, 'GetReports.xml'))
    
    # Insert sessionToken into this query.
    data.find(
      './/{http://archer-tech.com/webservices/}sessionToken'
    ).text = self.auth.token

    headers = {
      'Accept': 'text/xml; charset=utf-8',
      'Content-Type': 'text/xml; charset=utf-8',
      'SOAPAction': 'http://archer-tech.com/webservices/GetReports'
    }

    # ArcherAuth maintains the session state.
    response = self.auth.session.post(
      url,
      data = ET.tostring(data.getroot()),
      headers = headers
    )

    # The root of our search is the result of our query.
    root = ET.fromstring(
      ET.fromstring(
        response.text
      ).find(
        './/{http://archer-tech.com/webservices/}GetReportsResult'
      ).text
    )

    # Map report name to GUID and lookup by name.
    try:
      guid = {element.find('ReportName').text: element.find('ReportGUID').text
              for element
              in root.findall('ReportValue')}[name]
    except KeyError:
      raise ValueError('Invalid name.')
    
    return guid

  def get_search_options(self, guid: str) -> ET.Element:
    """
    Get search options for Execute Search. Requires report GUID.
    Use get_report_guid if report name is known, but GUID is not.

    API Used: Web Services

    Positional arguments:
    guid -- GUID of report for which we return the associated Search Options.
    """

    url = f'{self.auth.base_url}/ws/search.asmx'
    
    data = ET.parse(
      pkg_resources.open_text(templates, 'GetSearchOptionsByGuid.xml')
    )
    
    data.find(
      './/{http://archer-tech.com/webservices/}sessionToken'
    ).text = self.auth.token

    data.find(
      './/{http://archer-tech.com/webservices/}searchReportGuid'
    ).text = guid

    headers = {
      'Accept': 'text/xml; charset=utf-8',
      'Content-Type': 'text/xml; charset=utf-8',
      'SOAPAction': 'http://archer-tech.com/webservices/GetSearchOptionsByGuid'
    }

    response = self.auth.session.post(
      url,
      data = ET.tostring(data.getroot()),
      headers = headers
    )

    # Isolate Search Options returned by our query.
    options = ET.fromstring(
      ET.fromstring(
        response.text
      ).find(
        './/{http://archer-tech.com/webservices/}GetSearchOptionsByGuidResult'
      ).text
    )
    
    # Set PageSize. (i.e. Set the number of records returned per API query.)
    options.find(
      './/PageSize'
    ).text = str(self.page_size)

    return options

  def _search_pages(self, url: str, data: ET.ElementTree,
                    headers: dict, page_num: int) -> ET.Element:
    """Helper method for exec_search to query all pages.

    API Used: Web Services

    Positional arguments:
    url -- Post request url.
    data -- Post request data. pageNumber will always update to page_num.
    headers -- Post request headers.
    page_num -- Page number to query. Starts at 1, increments by 1.
    """

    data.find(
      './/{http://archer-tech.com/webservices/}pageNumber'
    ).text = str(page_num)

    response = self.auth.session.post(
      url,
      data = ET.tostring(data.getroot()),
      headers = headers
    )

    result = ET.fromstring(
      ET.fromstring(
        response.text
      ).find('.//{http://archer-tech.com/webservices/}ExecuteSearchResult').text
    )

    # num_pages = Ceiling(Number of records / PageSize)
    num_pages = -(-int(result.attrib['count']) // self.page_size)

    if page_num == num_pages:
      return result
    else:
      search = self._search_pages(url, data, headers, page_num + 1)
      
      for record in result.findall('.//Record'):
        search.append(record)

      return search

  def exec_search(self, options: ET.Element) -> dict:
    """
    Execute Search with provided Search Options.

    API Used: Web Services

    Positional arguments:
    options -- Search Options
    """

    url = f'{self.auth.base_url}/ws/search.asmx'
    
    data = ET.parse(pkg_resources.open_text(templates, 'ExecuteSearch.xml'))
    
    data.find(
      './/{http://archer-tech.com/webservices/}sessionToken'
    ).text = self.auth.token

    data.find(
      './/{http://archer-tech.com/webservices/}searchOptions'
    ).text = ET.tostring(options, encoding = 'unicode')

    headers = {
      'Accept': 'text/xml; charset=utf-8',
      'Content-Type': 'text/xml; charset=utf-8',
      'SOAPAction': 'http://archer-tech.com/webservices/ExecuteSearch'
    }

    result = self._search_pages(url, data, headers, 1)

    # Map field id to field name.
    map_fields = {
      field_def.attrib['id']: re.sub(
        '\W+_*|_+',
        '_',
        field_def.attrib['name'].strip().lower())
      for field_def
      in result.findall('.//FieldDefinition')
    }

    search = {map_fields[field]: [] for field in map_fields}

    for record in result.findall('.//Record'):
      for field in record.findall('Field'):
        if field.attrib['id'] in map_fields:
          search[
            map_fields[field.attrib['id']]
          ].append(field.text)

    return search

  def get_history_log(self, id) -> pd.DataFrame:
    """
    Get history log data.

    API Used: RESTful

    Positional arguments:
    id -- Tracking ID of record to query for history log data.
    """
    url = f'{self.auth.base_url}/platformapi/core/content/history/{id}'
    headers = {'X-Http-Method-Override': 'GET'}
  
    response = self.auth.session.post(url, headers = headers)

    history_audits = response.json()[0]['RequestedObject']['HistoryAudits']

    for audit in history_audits:
      temp = []
      for field in audit['FieldHistory']:
        temp.append(audit['FieldHistory'][field])
      audit['FieldHistory'] = temp

    return pd.json_normalize(
      history_audits,
      record_path = ['FieldHistory'],
      meta = ['Id',
              'HistoryAction',
              'Type',
              'ContentId',
              'ActionDate',
              'ActionUserId']
    ).rename(
      columns = lambda name: re.sub('(?<!^)(?=[A-Z])', '_', name).lower()
    )

  def get_history_logs(self) -> pd.DataFrame:
    """
    Get all history log data under current context.
    """
    if not self.contextualized:
      raise ContextError(
        'Context not set. You must call set_context following instantiation.'
      )

    dfs = []

    for id in self.context['tracking_id']:
      dfs.append(self.get_history_log(id))

    return pd.concat(dfs).reset_index(drop = True)

  def set_context(self, report_name: str) -> None:
    """
    Establish context under which 's' methods will execute.

    s methods:
    - get_history_logs()

    Can be called following instantiation.

    Positional arguments:
    report_name -- Name of OPTS report.
    """
    report_guid = self.get_report_guid(report_name)
    search_options = self.get_search_options(report_guid)

    self.context = pd.DataFrame(self.exec_search(search_options))
    self.contextualized = True

  def get_endpoints(self) -> list:
    """
    Get Content API endpoints. Returned to user and used to validate future
    Content API queries.

    API Used: Content
    """
    url = f'{self.auth.base_url}/contentapi'
    headers = {'Cache-Control': 'no-cache'}

    response = self.auth.session.get(
      url,
      headers = headers
    )

    endpoints = {}

    for endpoint in response.json()['value']:
      if endpoint['kind'] == 'EntitySet':
        endpoints[endpoint['name']] = endpoint['url']
      else:
        # Please file a bug report if you recieve this warning.
        warnings.warn('Non-EntitySet found in endpoints.', Warning)

    self.endpoints = endpoints
    self.last_refresh = datetime.datetime.now()

    return list(endpoints.keys())
  
  def get_level_metadata(self, level_alias: str) -> list:
    """
    Query Content API. Max 1000 contents per API call. This function returns
    all contents as a json array.

    API Used: Content

    Positional arguments:
    level_alias -- Level alias returned by get_endpoints()
    """
    try:
      if self.last_refresh is None:
        self.get_endpoints()
      url = f'{self.auth.base_url}/contentapi/{self.endpoints[level_alias]}'
    except KeyError:
      raise ValueError('''Invalid level_alias. Please check your alias or call
                       get_endpoints() to refresh the endpoints dictionary.''')
    
    headers = {'Cache-Control': 'no-cache'}
    params = {'skip': 0}

    content = []

    while(True): # see PEP 315
      response = self.auth.session.get(
        url,
        headers = headers,
        params = params
      )

      if len(response.json()['value']) == 0:
        break

      content = content + response.json()['value']
      params['skip'] = params['skip'] + len(response.json()['value'])

    return content
  
  def get_levels_metadata(self, level_aliases: list) -> dict:
    """
    Get level metadata for a list of levels.

    Positional arguments:
    level_aliases -- Level aliases returned by get_endpoints()
    """
    contents = dict.fromkeys(level_aliases)

    for alias in level_aliases:
      contents[alias] = self.get_level_metadata(alias)

    return contents

  def __init__(self, auth: 'ArcherAuth') -> None:
    self.auth = auth
    self.context = None # RESTful
    self.contextualized = False # RESTful
    self.endpoints = None # Content
    self.last_refresh = None # Content
    self.page_size = 1000 # Web Services