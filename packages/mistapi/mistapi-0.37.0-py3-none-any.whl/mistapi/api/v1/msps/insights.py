'''
--------------------------------------------------------------------------------
------------------------- Mist API Python CLI Session --------------------------

    Written by: Thomas Munzer (tmunzer@juniper.net)
    Github    : https://github.com/tmunzer/mistapi_python

    This package is licensed under the MIT License.

--------------------------------------------------------------------------------
'''

from mistapi import APISession as _APISession
from mistapi.__api_response import APIResponse as _APIResponse

def getMspSle(mist_session:_APISession, msp_id:str, metric:str, sle:str=None, duration:str="1d", interval:str=None, start:int=None, end:int=None) -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/getMspSle
    
    PARAMS
    -----------
    :param APISession mist_session - mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    :param str msp_id
    :param str metric - see /api/v1/const/insight_metrics for available metrics        
    
    QUERY PARAMS
    ------------
    :param str sle - see /api/v1/const/insight_metrics for more details
    :param str duration
    :param str interval
    :param int start
    :param int end        
    
    RETURN
    -----------
    :return APIResponse - response from the API call
    """
    uri = f"/api/v1/msps/{msp_id}/insights/{metric}"
    query_params={}
    if sle: query_params["sle"]=sle
    if duration: query_params["duration"]=duration
    if interval: query_params["interval"]=interval
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    