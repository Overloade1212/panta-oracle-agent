#!/usr/bin/env python3
"""
Panta Oracle Agent — Main CLI
Autonomous Prediction Market Intelligence & Trading Agent on Solana.
"""

import argparse
import asyncio
import os
import sys

from config import OracleConfig
from oracle_brain import OracleBrain
from panta_client import PantaClient
from ui import OracleUI

def parse_args():
    parser = argparse.ArgumentParser(
        description="🔮 Panta Oracle Agent: Autonomous Prediction Market Intelligence on Solana"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        default=True,
        help="Run in demo showcase mode with verified Panta markets buffer (Default: True)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Connect to live Panta Markets API endpoint"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.getenv("PANTA_API_KEY"),
        help="Panta Markets API Key"
    )
    parser.add_argument(
        "--bankroll",
        type=float,
        default=1000.0,
        help="Portfolio bankroll in USDC for Kelly Criterion calculations (Default: $1,000)"
    )
    parser.add_argument(
        "--min-ev",
        type=float,
        default=0.10,
        help="Minimum Expected Value threshold to trigger trade signals (Default: 0.10 = +10%%)"
    )
    return parser.parse_args()

async def main():
    args = parse_args()
    
    config = OracleConfig(
        api_key=args.api_key,
        bankroll_usdc=args.bankroll,
        min_ev_threshold=args.min_ev,
        demo_mode=args.demo if not args.live else False
    )
    
    client = PantaClient(config)
    brain = OracleBrain(
        min_ev_threshold=config.min_ev_threshold,
        max_kelly_fraction=config.max_kelly_fraction
    )
    ui = OracleUI(bankroll_usdc=config.bankroll_usdc)
    
    try:
        # 1. Fetch prediction markets from Panta
        markets = await client.fetch_markets()
        
        # 2. Evaluate markets using Bayesian & EV models
        opportunities = brain.scan_opportunities(markets, bankroll_usdc=config.bankroll_usdc)
        
        # 3. Build trade order for top opportunity
        top_order = None
        if opportunities:
            top_order = await client.build_trade_order(opportunities[0])
            
        # 4. Render Rich Dashboard
        ui.render_dashboard(opportunities, top_order)
        
    finally:
        await client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
