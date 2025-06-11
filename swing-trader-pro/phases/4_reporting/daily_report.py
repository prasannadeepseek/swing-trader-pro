# phases/4_reporting/daily_report.py
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
