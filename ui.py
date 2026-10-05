"""
Terminal User Interface for Panta Oracle Agent
Renders prediction market opportunity tables, risk meters, and execution orders using Rich.
"""

from typing import Dict, List
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from oracle_brain import OpportunityAnalysis, PredictionMarket

class OracleUI:
    def __init__(self, bankroll_usdc: float = 1000.0):
        self.console = Console()
        self.bankroll_usdc = bankroll_usdc

    def render_dashboard(
        self,
        opportunities: List[OpportunityAnalysis],
        top_order: Dict
    ):
        self.console.clear()
        
        # 1. Header Panel
        self.console.print(self._build_header(len(opportunities)))
        self.console.print()
        
        # 2. Opportunities Table
        self.console.print(self._build_opportunities_table(opportunities))
        self.console.print()
        
        # 3. Top Trade Execution Card
        if top_order and opportunities:
            self.console.print(self._build_execution_card(opportunities[0], top_order))
            self.console.print()
            
        # 4. Footer
        self.console.print(self._build_footer())

    def _build_header(self, opps_count: int) -> Panel:
        title = Text.from_markup(
            "🔮 [bold cyan]PANTA ORACLE AGENT[/bold cyan] [white]v1.0.0[/white] │ "
            "[bold magenta]Autonomous Prediction Market Trading & Intelligence[/bold magenta]\n"
            "[dim]Integrated with Panta Markets Protocol (Solana Mainnet) │ Bayesian Inference + Kelly Sizing[/dim]"
        )
        stats = Text.from_markup(
            f"[bold white]Portfolio Bankroll:[/bold white] [bold green]${self.bankroll_usdc:,.2f} USDC[/bold green] │ "
            f"[bold white]Edge Threshold:[/bold white] [bold yellow]>= +10.0% EV[/bold yellow] │ "
            f"[bold white]Alpha Signals Found:[/bold white] [bold cyan]{opps_count}[/bold cyan]"
        )
        grid = Table.grid(expand=True)
        grid.add_column(ratio=1)
        grid.add_column(ratio=1, justify="right")
        grid.add_row(title, stats)
        return Panel(grid, style="cyan", border_style="bold blue")

    def _build_opportunities_table(self, opportunities: List[OpportunityAnalysis]) -> Panel:
        table = Table(expand=True, box=None, padding=(0, 1), show_edge=False)
        table.add_column("Market Event", style="white", ratio=4)
        table.add_column("Category", style="dim", ratio=2)
        table.add_column("Action", justify="center", width=8)
        table.add_column("Market Px", justify="right", width=10)
        table.add_column("Fair Px", justify="right", width=10)
        table.add_column("Edge", justify="right", width=9)
        table.add_column("EV Yield", justify="right", width=11)
        table.add_column("Kelly Bet", justify="right", width=12)
        table.add_column("Confidence", justify="center", width=11)

        for opp in opportunities:
            side_color = "bold green" if opp.recommended_side == "YES" else "bold red"
            side_badge = f"[{side_color}]{opp.recommended_side}[/{side_color}]"
            
            mkt_pct = f"{opp.market_price * 100:.1f}¢"
            fair_pct = f"{opp.fair_yes_prob * 100:.1f}¢" if opp.recommended_side == "YES" else f"{(1 - opp.fair_yes_prob) * 100:.1f}¢"
            edge_str = f"+{opp.edge_pct:.1f}%" if opp.edge_pct >= 0 else f"{opp.edge_pct:.1f}%"
            edge_styled = f"[bold green]{edge_str}[/bold green]" if opp.edge_pct >= 0 else f"[red]{edge_str}[/red]"
            
            ev_str = f"[bold yellow]+{opp.expected_value * 100:.1f}%[/bold yellow]"
            bet_str = f"[bold cyan]${opp.recommended_size_usdc:.2f}[/bold cyan]"
            conf_str = f"[magenta]{opp.confidence_score * 100:.0f}%[/magenta]"
            
            table.add_row(
                opp.market.title,
                opp.market.category,
                side_badge,
                mkt_pct,
                fair_pct,
                edge_styled,
                ev_str,
                bet_str,
                conf_str
            )

        return Panel(table, title="[bold white]📊 Panta Market Inefficiencies & Positive EV Signals[/bold white]", border_style="cyan")

    def _build_execution_card(self, opp: OpportunityAnalysis, order: Dict) -> Panel:
        side_color = "green" if order["side"] == "YES" else "red"
        
        info = Text.from_markup(
            f"🎯 [bold white]Top Alpha Opportunity:[/bold white] [yellow]{opp.market.title}[/yellow]\n"
            f"💡 [bold white]AI Rationale:[/bold white] [dim]{opp.rationale}[/dim]\n"
            f"⚡ [bold white]Order Side:[/bold white] [bold {side_color}]{order['side']}[/bold {side_color}]  │  "
            f"[bold white]Stake:[/bold white] [bold green]${order['total_cost_usdc']:.2f} USDC[/bold green]  │  "
            f"[bold white]Contracts:[/bold white] [cyan]{order['contracts_purchased']}[/cyan]  │  "
            f"[bold white]Max Payout:[/bold white] [bold yellow]${order['max_payout_usdc']:.2f} USDC[/bold yellow]  │  "
            f"[bold white]Expected Net Profit:[/bold white] [bold green]+${order['expected_profit_usdc']:.2f} USDC[/bold green]\n"
            f"⛓️  [bold white]Solana Transaction:[/bold white] [dim]Ready to sign via Panta Market Program ({order['solana_program_id'][:8]}...)[/dim]"
        )
        return Panel(info, title="[bold green]🚀 Autonomous Trade Execution Spec (Panta Protocol)[/bold green]", border_style="green")

    def _build_footer(self) -> Panel:
        footer = Text.from_markup(
            "[dim]Developer: [bold cyan]Anatoli Kolotovkin (@Overloade1212)[/bold cyan] │ "
            "Submission for [bold magenta]Colosseum Crypto World's Fair — Panta API Sidetrack[/bold magenta][/dim]"
        )
        return Panel(Align.center(footer), style="dim", border_style="dim")
