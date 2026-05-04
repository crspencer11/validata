import click
import json
import logging
from src.engine import DataValidator
from src.rules import PriceSpikeRule, MonotonicTimeRule

logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('--input', type=str, required=True, help='Path to the input JSON file containing financial data.')
@click.option('--threshold', type=float, default=0.10, help='Threshold percentage for price spike validation.')
@click.option('--repair', is_flag=True, help='Enable repair mode to suggest fixes for data issues.')
def main(input, threshold, repair):
    """Command-line interface for the Financial Data Validator."""
    logging.info("Loading data from %s", input)
    
    try:
        with open(input, 'r') as f:
            data = json.load(f)
    except Exception as e:
        logging.error("Error loading data: %s", e)
        return

    rules = [PriceSpikeRule(threshold), MonotonicTimeRule()]
    validator = DataValidator(rules)

    result = validator.run(data)
    logging.info("Validation result: %s", result)

    if repair:
        # Implement repair logic here
        logging.info("Repair mode is enabled. Suggesting fixes...")
        # Example: Call a repair function from repair.py
        # repaired_data = repair_data(data)
        # logging.info("Repaired data: %s", repaired_data)

if __name__ == '__main__':
    main()