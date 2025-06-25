# sqlquerygen

`sqlquerygen` is a tool designed to generate SQL queries programmatically, making it easier for developers to interact with databases without manually writing SQL statements. This project aims to streamline query generation, reduce human error, and speed up backend development workflows.

## Features

- Generate SQL queries for CRUD operations (Create, Read, Update, Delete)
- Support for multiple SQL dialects (MySQL, PostgreSQL, SQLite, etc.)
- Parameterized query support for security against SQL injection
- Easy-to-use API for integrating with other Python projects
- Extensible architecture for adding custom query templates

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Getting Started

These instructions will help you set up and start using `sqlquerygen` in your project.

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ASHOKEKUMAR-S/sqlquerygen.git
cd sqlquerygen
pip install -r requirements.txt
```

Or install via pip (if published as a package):

```bash
pip install sqlquerygen
```

## Usage

Here’s a basic example of how to use `sqlquerygen`:

```python
from sqlquerygen import QueryGenerator

qg = QueryGenerator(dialect="mysql")
query = qg.select(
    table="users",
    columns=["id", "name", "email"],
    where={"active": True}
)

print(query)  # Outputs: SELECT id, name, email FROM users WHERE active=1;
```

### Supported Dialects

- MySQL
- PostgreSQL
- SQLite

## API Reference

| Method         | Description                               |
| -------------- | ----------------------------------------- |
| `select`       | Generate SELECT queries                   |
| `insert`       | Generate INSERT queries                   |
| `update`       | Generate UPDATE queries                   |
| `delete`       | Generate DELETE queries                   |

See the [API documentation](docs/API.md) for detailed usage.

## Configuration

You can configure the query generator for your specific needs via the constructor:

```python
qg = QueryGenerator(dialect="postgresql", safe_mode=True)
```

## Examples

- See [examples/example_basic.py](examples/example_basic.py) for a simple use case.
- See [examples/example_advanced.py](examples/example_advanced.py) for advanced usage.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- Fork the repository
- Create your feature branch (`git checkout -b feature/AmazingFeature`)
- Commit your changes (`git commit -m 'Add some AmazingFeature'`)
- Push to the branch (`git push origin feature/AmazingFeature`)
- Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Maintainer: [ASHOKEKUMAR-S](https://github.com/ASHOKEKUMAR-S)

For questions or support, please open an issue.
