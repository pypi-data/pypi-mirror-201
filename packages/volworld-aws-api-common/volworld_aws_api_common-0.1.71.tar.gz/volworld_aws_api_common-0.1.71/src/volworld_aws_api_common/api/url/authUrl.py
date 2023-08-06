from typing import Final

from volworld_aws_api_common.api.AA import AA

from volworld_aws_api_common.test.aws.url import build_api_root_url, build_url

ROOT__: Final[str] = build_api_root_url(AA.Auth)

doSignupUrl: Final[str] = build_url(ROOT__, AA.Signup)

doLoginUrl: Final[str] = build_url(ROOT__, AA.Login)

# doLogoutUrl: Final[str] = build_url(ROOT__, AA.Logout)

currentUserUrl: Final[str] = build_url(ROOT__, AA.UserId)
