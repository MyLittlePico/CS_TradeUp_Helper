import argparse
import os

from src.fetch_inventory import get_inventory_csv


def main():
    parser = argparse.ArgumentParser(description="Steam TradeUp Helper")
    parser.add_argument(
        "--fetch", 
        action="store_true", 
        help="Fetch data from the API and initialize the CSV file"
    )
    

    args = parser.parse_args()

    if args.fetch:
        get_inventory_csv()
    
if __name__ == "__main__":
    main()
