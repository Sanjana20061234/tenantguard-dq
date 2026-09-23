# Demo Script

1. `make install` - Installs package.
2. `make data` - Generates clean and corrupt data.
3. `make test` - Runs unit tests instantly without a DB.
4. `dq generate` - Auto-generates rules from catalog.
5. `dq demo --backend duckdb` - Runs the clean data (Exit 0) and the corrupt data (Exit 1).
6. Show that canary string `SECRET_PII_CANARY_123` is missing from all logs and output.
7. Show CI workflow blocking bad YAML.
