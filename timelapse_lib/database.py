import sqlite3
import re
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "timelapse.db"


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_db():
    """Initialize the database schema."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_path TEXT NOT NULL UNIQUE,
            captured_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_id INTEGER NOT NULL UNIQUE,
            description TEXT NOT NULL,
            plant_score REAL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(photo_id) REFERENCES photos(id)
        )
    """)
    
    conn.commit()
    conn.close()


def store_photo(photo_path, captured_at=None):
    """Store a photo in the database. Returns the photo ID."""
    if captured_at is None:
        captured_at = datetime.now()
    
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute(
            "INSERT INTO photos (photo_path, captured_at) VALUES (?, ?)",
            (str(photo_path), captured_at)
        )
        conn.commit()
        photo_id = c.lastrowid
        return photo_id
    except sqlite3.IntegrityError:
        # Photo already exists, get its ID
        c.execute("SELECT id FROM photos WHERE photo_path = ?", (str(photo_path),))
        row = c.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def store_analysis(photo_id, description, plant_score=None):
    """Store AI analysis for a photo."""
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute(
            "INSERT INTO ai_analysis (photo_id, description, plant_score) VALUES (?, ?, ?)",
            (photo_id, description, plant_score)
        )
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        # Analysis already exists for this photo, update it
        c.execute(
            "UPDATE ai_analysis SET description = ?, plant_score = ? WHERE photo_id = ?",
            (description, plant_score, photo_id)
        )
        conn.commit()
        return photo_id
    finally:
        conn.close()


def extract_plant_score(description):
    """Extract a numeric plant score from the AI description (0-100).
    
    Looks for patterns like "Score: 85" or "Plant Health: 7/10" etc.
    Returns None if no score found.
    """
    # Try to find patterns like "Score: 85" or "score of 85"
    match = re.search(r'[Ss]core[:\s]+(\d+)', description)
    if match:
        score = int(match.group(1))
        if 0 <= score <= 100:
            return score
    
    # Try to find patterns like "7/10" and convert to 0-100 scale
    match = re.search(r'(\d+)\s*/\s*10', description)
    if match:
        score = int(match.group(1))
        if 0 <= score <= 10:
            return (score / 10) * 100
    
    return None


def get_latest_analysis():
    """Get the most recent AI analysis."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT p.photo_path, p.captured_at, a.description, a.plant_score, a.analyzed_at
        FROM ai_analysis a
        JOIN photos p ON a.photo_id = p.id
        ORDER BY a.analyzed_at DESC
        LIMIT 1
    """)
    
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_analyses_since(days_ago=7):
    """Get all AI analyses from the past N days."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT p.photo_path, p.captured_at, a.description, a.plant_score, a.analyzed_at
        FROM ai_analysis a
        JOIN photos p ON a.photo_id = p.id
        WHERE a.analyzed_at >= datetime('now', '-' || ? || ' days')
        ORDER BY a.analyzed_at DESC
    """, (days_ago,))
    
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_plant_score_history(limit=30):
    """Get plant score history for charting/analysis."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT p.captured_at, a.plant_score
        FROM ai_analysis a
        JOIN photos p ON a.photo_id = p.id
        WHERE a.plant_score IS NOT NULL
        ORDER BY p.captured_at DESC
        LIMIT ?
    """, (limit,))
    
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
