from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str

class DatabaseConnection:
    # Static registry to store instances
    _instances: Dict[str, 'DatabaseConnection'] = {}
    
    def __init__(self, config: DatabaseConfig) -> None:
        """Private constructor, should not be called directly"""
        self.config = config
        self.connected = False
    
    @classmethod
    def get_connection(cls, db_name: str, config: Optional[DatabaseConfig] = None) -> 'DatabaseConnection':
        """
        Get or create a database connection for the specified database name
        
        Args:
            db_name: Unique identifier for the database connection
            config: Configuration for new connection (required only for first access)
        
        Returns:
            DatabaseConnection instance for the specified database
        """
        if db_name not in cls._instances:
            if config is None:
                raise ValueError(f"Configuration required for new database: {db_name}")
            cls._instances[db_name] = cls(config)
        
        return cls._instances[db_name]
    
    def connect(self) -> None:
        """Simulate database connection"""
        if not self.connected:
            print(f"Connecting to {self.config.database} at {self.config.host}:{self.config.port}")
            self.connected = True

# Usage Example
users_db_config = DatabaseConfig(
    host="users.example.com",
    port=5432,
    database="users",
    username="admin",
    password="secret"
)

products_db_config = DatabaseConfig(
    host="products.example.com",
    port=5432,
    database="products",
    username="admin",
    password="secret"
)

# First access creates new instances
users_db = DatabaseConnection.get_connection("users", users_db_config)
users_db.connect()
products_db = DatabaseConnection.get_connection("products", products_db_config)
products_db.connect()

# Subsequent accesses return existing instances
users_db_again = DatabaseConnection.get_connection("users")  # Same instance as users_db
users_db_again.connect() # Already connected, print nothing
products_db_again = DatabaseConnection.get_connection("products")  # Same instance as products_db
products_db_again.connect() # Already connected, print nothing