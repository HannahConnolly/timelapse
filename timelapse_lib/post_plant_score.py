import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import requests
from timelapse_lib.config import get_ai_webhook_url
import os

def generate_plant_score_chart():
    """Generate the plant score chart and return the file path."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'timelapse.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all plant scores with timestamps
    cursor.execute("""
        SELECT ai_analysis.plant_score, ai_analysis.analyzed_at, photos.captured_at
        FROM ai_analysis
        JOIN photos ON ai_analysis.photo_id = photos.id
        ORDER BY photos.captured_at
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    plant_scores = [row[0] for row in rows]
    timestamps = [datetime.fromisoformat(row[2]) for row in rows]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.plot(timestamps, plant_scores, marker='o', linestyle='-', linewidth=2, markersize=6, color='#2ecc71')
    ax.fill_between(timestamps, plant_scores, alpha=0.3, color='#2ecc71')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Plant Score', fontsize=12, fontweight='bold')
    ax.set_title('Plant Health Score Over Time', fontsize=14, fontweight='bold')
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha='right')
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Tight layout
    plt.tight_layout()
    
    # Save the plot
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(base_dir, 'plant_score_chart.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def post_plant_score_to_discord():
    """Generate and post the plant score chart to Discord AI channel."""
    chart_path = generate_plant_score_chart()
    
    if not chart_path:
        print("❌ No plant score data available")
        return
    
    webhook_url = get_ai_webhook_url()
    if not webhook_url:
        print("⚠️ AI webhook URL not configured. Cannot send chart.")
        return
    
    message = "📊 **Weekly Plant Health Report**\n\nHere's your plant's health score trend for this week!"
    
    try:
        with open(chart_path, 'rb') as f:
            files = {'file': f}
            data = {'content': message}
            response = requests.post(webhook_url, data=data, files=files, timeout=10)
        
        if response.ok:
            print(f"✅ Plant score chart posted to Discord successfully")
        else:
            print(f"❌ Discord error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Error posting to Discord: {e}")

if __name__ == "__main__":
    post_plant_score_to_discord()
