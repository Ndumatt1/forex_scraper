import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import humanize

def create_email_body(data):
    body = "Hello,\n\nHere is the latest update on Forex signals:\n\n"
    valid_signals = []
    # Iterate through signals
    for signal in data:
        # Check if 'posted' key exists
        if 'posted' in signal:
            # Parse the 'posted' time using humanize
            posted_time = humanize.naturaltime(signal['posted'])

            # Check if the signal was posted in the last 2 minutes
            if 'minutes' in posted_time and int(posted_time.split()[0]) <= 3:
                valid_signals.append(signal)
    if not valid_signals:
        return None
    
    for signal in valid_signals:

        body += f"\nCurrency Pair: {signal['currency_pair']}\n"
        # Check if 'Buy at' key exists
        buy_at_key = 'Buy at'
        if buy_at_key in signal:
            body += f"{buy_at_key}: {signal[buy_at_key]}\n"
        
        # Check if 'Sell at' key exists
        sell_at_key = 'Sell at'
        if sell_at_key in signal:
            body += f"{sell_at_key}: {signal[sell_at_key]}\n"

        # Check if 'Take profit* at' key exists
        take_profit_key = 'Take profit* at'
        if take_profit_key in signal:
            body += f"{take_profit_key.replace('*', '')}: {signal[take_profit_key]}\n"

        # Check if 'Stop loss at' key exists
        stop_loss_key = 'Stop loss at'
        if stop_loss_key in signal:
            body += f"{stop_loss_key}: {signal[stop_loss_key]}\n"

        body += f"Posted: {signal['posted']}\n\n"

    body += "Thank you for using our Forex signals service!\n\nBest regards,\nThe Forex Signals Team"
    return body
