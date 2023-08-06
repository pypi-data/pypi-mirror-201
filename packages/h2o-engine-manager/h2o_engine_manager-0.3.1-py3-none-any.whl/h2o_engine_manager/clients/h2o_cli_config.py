import toml


class CLIConfig:
    def __init__(self, path) -> None:
        """Read H2O CLI config file from given path.
        Errors are ignored and the config is set to None if the file cannot be read.

        Args:
            path: (str, optional): Path to the H2O CLI config file.
        """
        try:
            h2o_cfg = toml.load(path)
        except:
            self.token = None
            self.url = None
            return

        # Read token and URL from the H2O CLI config.
        if "PlatformToken" in h2o_cfg:
            self.token = h2o_cfg["PlatformToken"]
        else:
            self.token = None

        if "Endpoint" in h2o_cfg:
            self.url = h2o_cfg["Endpoint"]
        else:
            self.url = None
