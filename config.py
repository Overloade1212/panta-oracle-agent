"""
Panta Oracle Agent Configuration
Configures Panta Markets API base URLs, risk parameters, and Solana RPC settings.
"""

import os
from dataclasses import dataclass
from typing import Optional

# Panta Markets API Endpoints
PANTA_API_BASE_URL = os.getenv("PANTA_API_BASE_URL", "https://live-api.panta.market/api/v1")
PANTA_STAGING_BASE_URL = "https://staging-api.panta.market/api/v1"

# Solana RPC Endpoint
DEFAULT_SOLANA_RPC = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")

# Quantitative Risk & Oracle Parameters
DEFAULT_MIN_EV_THRESHOLD = float(os.getenv("MIN_EV_THRESHOLD", "0.10"))  # 10% edge
DEFAULT_MAX_KELLY_FRACTION = float(os.getenv("MAX_KELLY_FRACTION", "0.25"))  # Quarter-Kelly for safety
DEFAULT_BANKROLL_USDC = float(os.getenv("DEFAULT_BANKROLL_USDC", "1000.0"))

@dataclass
class OracleConfig:
    api_key: Optional[str] = os.getenv("PANTA_API_KEY")
    api_base_url: str = PANTA_API_BASE_URL
    solana_rpc: str = DEFAULT_SOLANA_RPC
    min_ev_threshold: float = DEFAULT_MIN_EV_THRESHOLD
    max_kelly_fraction: float = DEFAULT_MAX_KELLY_FRACTION
    bankroll_usdc: float = DEFAULT_BANKROLL_USDC
    demo_mode: bool = True
