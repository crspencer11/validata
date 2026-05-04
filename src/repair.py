class DataRepairer:
    @staticmethod
    def interpolate_missing_prices(data: list[dict]) -> list[dict]:
        """Suggests fixes for missing price points by linear interpolation."""
        prices = [entry['price'] for entry in data if 'price' in entry]
        timestamps = [entry['timestamp'] for entry in data if 'price' in entry]
        
        if not prices or len(prices) < 2:
            return data  # Not enough data to interpolate
        
        for i in range(len(data)):
            if 'price' not in data[i]:
                # Find the nearest previous and next prices
                prev_price = next((prices[j] for j in range(i-1, -1, -1) if 'price' in data[j]), None)
                next_price = next((prices[j] for j in range(i+1, len(data)) if 'price' in data[j]), None)
                
                if prev_price is not None and next_price is not None:
                    # Linear interpolation
                    data[i]['price'] = (prev_price + next_price) / 2
                elif prev_price is not None:
                    data[i]['price'] = prev_price  # Carry forward the last known price
                elif next_price is not None:
                    data[i]['price'] = next_price  # Carry backward the next known price
        
        return data

    @staticmethod
    def fix_time_order(data: list[dict]) -> list[dict]:
        """Suggests fixes for non-sequential timestamps."""
        for i in range(1, len(data)):
            if data[i]['timestamp'] <= data[i-1]['timestamp']:
                data[i]['timestamp'] = data[i-1]['timestamp'] + 1  # Increment timestamp by 1 second
        return data