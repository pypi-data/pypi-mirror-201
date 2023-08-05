class AWSRegionNotFound(Exception):
    pass


class LambdaConfigurationFileNotFound(Exception):
    pass


class LambdaConfigurationMissingValue(Exception):
    pass


class S3BucketNotFound(Exception):
    pass


class LambdaNotCreated(Exception):
    pass


class LicenseNotSpecified(Exception):
    pass


class LicenseNotValid(Exception):
    pass


class LicenseExpired(Exception):
    pass


class PythonVersionNotSupported(Exception):
    pass


class CommandExecutionException(Exception):
    pass


class UnsupportedInfraSetupTool(Exception):
    pass
