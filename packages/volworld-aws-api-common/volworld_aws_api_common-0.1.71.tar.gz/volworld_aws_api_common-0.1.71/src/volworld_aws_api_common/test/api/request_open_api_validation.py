from requests import Response
from volworld_common.test.Timer import Timer
from volworld_aws_api_common.api.AA import AA
from volworld_aws_api_common.test.aws.ATestRequest import ATestRequest
from volworld_aws_api_common.test.request import post_request, get_request
from volworld_aws_api_common.test.Url import Url

from volworld_aws_api_common.test.api.OpenApiValidation import OpenApiValidation


def request_open_api_post_validation(url: str, req, resp_json, resp: Response, attList):
    url = url.replace(Url.Root, '')
    url = url.replace('//', '/')

    val = OpenApiValidation()
    val.validate_POST_request(req, url, attList)

    print("[db_fn_open_api_validation] res = ", resp_json)
    print("[db_fn_open_api_validation] resp.status_code = ", resp.status_code)
    if AA.___Error___ not in resp_json:
        val.validate_POST_response({
            AA.Data: resp_json[AA.Data]
        }, url, resp.status_code, attList)
    else:
        val.validate_POST_response({
            AA.___Error___: resp_json[AA.___Error___]
        }, url, resp.status_code, attList)


def request_open_api_get_validation(url: str, resp_json, resp: Response, attList):
    url = url.replace(Url.Root, '')
    url = url.replace('//', '/')

    val = OpenApiValidation()

    print("[db_fn_open_api_validation] res = ", resp_json)
    print("[db_fn_open_api_validation] resp.status_code = ", resp.status_code)
    if AA.___Error___ not in resp_json:
        val.validate_GET_response({
            AA.Data: resp_json[AA.Data]
        }, url, resp.status_code, attList)
    else:
        val.validate_GET_response({
            AA.___Error___: resp_json[AA.___Error___]
        }, url, resp.status_code, attList)

def post_request_with_validation(
        url: str, req: dict,
        test_req: ATestRequest, attList,
        token: str = None):
    with Timer(f"Call DB Function [{url}]"):
        resp_json, resp = post_request(url, req, test_req, attList, token=token)
    request_open_api_post_validation(url, req, resp_json, resp, attList)
    return resp_json, resp

def get_request_with_validation(
        url: str,
        test_req: ATestRequest, attList,
        params: dict = None,
        token: str = None):
    with Timer(f"Call DB Function [{url}]"):
        resp_json, resp = get_request(url, test_req, attList, params=params, token=token)
    request_open_api_get_validation(url, resp_json, resp, attList)
    return resp_json, resp