# Limitations

1. Globally unique ID assumption limits composite key handling.
2. Count-only diagnostics may make triage slightly more tedious for engineers.
3. Single-node ClickHouse for local docker is not production ready.
4. No Airflow / scheduler integration natively out of the box yet.
