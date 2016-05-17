import sepiida.errors

AuthenticationException = sepiida.errors.api_error(status_code=403, error_code='authentication-exception')
InvalidCredentials      = sepiida.errors.api_error(status_code=401, error_code='invalid-credentials')
ResourceDoesNotExist    = sepiida.errors.api_error(status_code=404, error_code='resource-does-not-exist')
