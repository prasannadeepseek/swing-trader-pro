# phases/4_reporting/daily_report.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from alerts.telegram import TelegramAlerts


class DailyReporter:
    def __init__(self):
        self.template = """
📊 *Daily Trading Report* - {date}
━━━━━━━━━━━━━━━━━━
🔹 Active Positions: {active_count}
🔹 P&L Today: ₹{daily_pnl:+,.2f}
🔹 Win Rate: {win_rate:.1%}
━━━━━━━━━━━━━━━━━━
📈 Best Performer: {top_symbol} (+{top_gain:.1%})
📉 Worst Performer: {bottom_symbol} ({bottom_gain:+.1%})
━━━━━━━━━━━━━━━━━━
{summary}
"""

    def generate(self, trades, positions):
        """Generate and send daily report"""
        report_data = self._compile_stats(trades, positions)
        message = self.template.format(**report_data)
        TelegramAlerts().send_report(message)

    def _compile_stats(self, trades, positions):
        """Compile trading statistics"""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'active_count': len(positions),
            'daily_pnl': sum(t['pnl'] for t in trades),
            'win_rate': len([t for t in trades if t['pnl'] > 0]) / len(trades),
            'top_symbol': max(trades, key=lambda x: x['pnl_pct'])['symbol'],
            'top_gain': max(t['pnl_pct'] for t in trades),
            'bottom_symbol': min(trades, key=lambda x: x['pnl_pct'])['symbol'],
            'bottom_gain': min(t['pnl_pct'] for t in trades),
            'summary': self._generate_summary(trades)
        }

# method 2 final version


class DailyReporter:
    """
    Generates and sends a daily trading report via Telegram.
    """

    def __init__(self, telegram_alerts: Optional[TelegramAlerts] = None):
        self.template = """
📊 *Daily Trading Report* - {date}
━━━━━━━━━━━━━━━━━━
🔹 Active Positions: {active_count}
🔹 P&L Today: ₹{daily_pnl:+,.2f}
🔹 Win Rate: {win_rate}
━━━━━━━━━━━━━━━━━━
📈 Best Performer: {top_symbol} ({top_gain})
📉 Worst Performer: {bottom_symbol} ({bottom_gain})
━━━━━━━━━━━━━━━━━━
{summary}
"""
        self.telegram_alerts = telegram_alerts or TelegramAlerts()

    def generate(self, trades: List[Dict[str, Any]], positions: List[Dict[str, Any]]) -> None:
        """
        Generate and send the daily trading report.

        Args:
            trades (List[Dict]): List of trade dictionaries with at least 'pnl', 'symbol', and 'pnl_pct'.
            positions (List[Dict]): List of active position dictionaries.
        """
        report_data = self._compile_stats(trades, positions)
        message = self.template.format(**report_data)
        self.telegram_alerts.send_report(message)

    def _compile_stats(self, trades: List[Dict[str, Any]], positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compile trading statistics for the report.

        Args:
            trades (List[Dict]): List of trade dictionaries.
            positions (List[Dict]): List of active position dictionaries.

        Returns:
            Dict[str, Any]: Compiled statistics for report template.
        """
        date_str = datetime.now().strftime('%Y-%m-%d')
        active_count = len(positions)
        daily_pnl = sum(t.get('pnl', 0) for t in trades)
        win_trades = [t for t in trades if t.get('pnl', 0) > 0]
        win_rate = f"{(len(win_trades) / len(trades)):.1%}" if trades else "N/A"

        if trades:
            top_trade = max(trades, key=lambda x: x.get('pnl_pct', 0))
            bottom_trade = min(trades, key=lambda x: x.get('pnl_pct', 0))
            top_symbol = top_trade.get('symbol', '-')
            top_gain = f"{top_trade.get('pnl_pct', 0):+.1%}"
            bottom_symbol = bottom_trade.get('symbol', '-')
            bottom_gain = f"{bottom_trade.get('pnl_pct', 0):+.1%}"
        else:
            top_symbol = bottom_symbol = "-"
            top_gain = bottom_gain = "N/A"

        summary = self._generate_summary(trades)

        return {
            'date': date_str,
            'active_count': active_count,
            'daily_pnl': daily_pnl,
            'win_rate': win_rate,
            'top_symbol': top_symbol,
            'top_gain': top_gain,
            'bottom_symbol': bottom_symbol,
            'bottom_gain': bottom_gain,
            'summary': summary
        }

    def _generate_summary(self, trades: List[Dict[str, Any]]) -> str:
        """
        Generate a summary string for the report.

        Args:
            trades (List[Dict]): List of trade dictionaries.

        Returns:
            str: Summary string.
        """
        if not trades:
            return "No trades executed today."
        winners = [t for t in trades if t.get('pnl', 0) > 0]
        losers = [t for t in trades if t.get('pnl', 0) <= 0]
        return (
            f"Winners: {len(winners)}, Losers: {len(losers)}. "
            f"Total Trades: {len(trades)}."
        )
