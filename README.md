# Validata

A CLI tool for validating and repairing financial time-series data.

## Why

Financial datasets often contain:
- sudden price spikes
- timestamp inconsistencies
- statistical anomalies

Validata helps detect and optionally repair these issues.

## Features

- Rule-based validation engine
- Repairable rules
- CLI interface
- JSON report output
- Statistical anomaly detection

## Usage

```bash
python -m src.cli --input data/sample_data.json
```
> Use the **--repair** flag for smart fixes
