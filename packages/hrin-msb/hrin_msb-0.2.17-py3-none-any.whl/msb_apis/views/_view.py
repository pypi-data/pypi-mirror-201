from msb_http import (ApiResponse)


def api_details(request=None, ver='', name=''):
	return ApiResponse.success(
		data=dict(method=request.method, version=ver, name=name)
	)
