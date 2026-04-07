import argparse
import os

from src.fetch_inventory import get_inventory_csv
from src.list_inventory import list_inventory_comps
from src.interface import interface
from src.apply_float_cap import apply_float_cap


def main():
    parser = argparse.ArgumentParser(description="Steam TradeUp Helper")
    parser.add_argument(
        "--fetch", 
        action="store_true", 
        help="Fetch data from the API and store as a local file"
    )
    parser.add_argument(
        "--comps", 
        action="store_true", 
        help="List components of your local inventory"
    )
    parser.add_argument(
        "--caps", 
        action="store_true", 
        help="List components of your local inventory"
    )

    args = parser.parse_args()

    if args.fetch:
        get_inventory_csv()
        return
    if args.comps:
        list_inventory_comps()
        return
    
    if args.caps:
        apply_float_cap()
        return

    interface()

    
    
if __name__ == "__main__":
    main()
