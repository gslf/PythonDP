class ConfigurationManager:
    # Class-level attribute to hold the Singleton instance
    _instance = None  

    def __new__(cls, *args, **kwargs):
        # Create the Singleton instance if it doesn't exist yet
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize the configuration with some default values
        self.settings = {
            "db_host": "localhost",
            "db_port": 5432,
            "debug_mode": True,
        }

    def update_setting(self, key, value):
        # Update a configuration setting
        self.settings[key] = value

    def get_setting(self, key):
        # Retrieve a configuration setting
        return self.settings.get(key)

# Test Singleton behavior
if __name__ == "__main__":
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()

    # Both instances should be the same
    print(f"Are config1 and config2 the same instance? {config1 is config2}")

    # Updating config in one instance should reflect in the other
    config1.update_setting("debug_mode", False)
    print(f"Debug mode in config2: {config2.get_setting('debug_mode')}")