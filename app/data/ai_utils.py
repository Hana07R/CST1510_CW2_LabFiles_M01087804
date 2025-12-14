import pandas as pd

def summarize_incidents(df: pd.DataFrame) -> str:
    if df.empty:
        return "No incidents to summarize."
    summary = f"Total Incidents: {len(df)}\n"
    if 'severity' in df.columns:
        severity_counts = df['severity'].value_counts().to_dict()
        summary += "Severity Breakdown:\n"
        for sev, count in severity_counts.items():
            summary += f"- {sev}: {count}\n"
    return summary

def summarize_threats(df: pd.DataFrame) -> str:
    if df.empty:
        return "No threats to summarize."
    summary = f"Total Threats: {len(df)}\n"
    if 'severity' in df.columns:
        severity_counts = df['severity'].value_counts().to_dict()
        summary += "Threat Severity Breakdown:\n"
        for sev, count in severity_counts.items():
            summary += f"- {sev}: {count}\n"
    return summary

def summarize_it_tickets(df: pd.DataFrame) -> str:
    if df.empty:
        return "No IT tickets to summarize."
    summary = f"Total IT Tickets: {len(df)}\n"
    if 'status' in df.columns:
        status_counts = df['status'].value_counts().to_dict()
        summary += "Ticket Status Breakdown:\n"
        for status, count in status_counts.items():
            summary += f"- {status}: {count}\n"
    return summary
