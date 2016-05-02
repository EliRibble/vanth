import sepiida.config

SPECIFICATION = {
    'api_token'             : sepiida.config.Option(str, 'api_token'),
    'secret_key'            : sepiida.config.Option(str, 'some-secret-key'),
    'session_cookie_domain' : sepiida.config.Option(str, None),
    'db'                    : sepiida.config.Option(str, 'postgres://vanth_dev:letmein@localhost:5432/vanth_test'),
    'debug'     : sepiida.config.Option(bool, True),
}
