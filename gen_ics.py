from datetime import datetime, timedelta, timezone
import json, re

# Read deadlines from index.html
with open('/sessions/vigilant-magical-carson/mnt/outputs/deadlines-site/index.html') as f:
    html = f.read()

# Extract the deadlines array
m = re.search(r'const deadlines = \[(.*?)\n\];', html, re.DOTALL)
arr_text = m.group(1)

# Parse each line that has a deadline object
items = []
for line in arr_text.split('\n'):
    obj_match = re.search(r"\{\s*course:\s*'([^']+)',\s*label:\s*'([^']+)',\s*date:\s*'([^']+)'(.*)\}", line)
    if not obj_match:
        continue
    course = obj_match.group(1)
    label = obj_match.group(2)
    date_str = obj_match.group(3)
    rest = obj_match.group(4)
    done = 'done: true' in rest
    note_match = re.search(r"note:\s*'([^']+)'", rest)
    note = note_match.group(1) if note_match else ''
    items.append({'course': course, 'label': label, 'date': date_str, 'done': done, 'note': note})

course_names = {'cs': 'CS 231', 'afm': 'AFM 231', 'math': 'CO 380', 'goals': 'Goal'}

# Only include not-done items
upcoming = [i for i in items if not i['done']]

# Generate ICS
lines = []
lines.append('BEGIN:VCALENDAR')
lines.append('VERSION:2.0')
lines.append('PRODID:-//Krish//Spring 2026 Deadlines//EN')
lines.append('CALSCALE:GREGORIAN')
lines.append('METHOD:PUBLISH')
lines.append('X-WR-CALNAME:Krish - Spring 2026 Deadlines')
lines.append('X-WR-CALDESC:Auto-updated tracker. Source: coolncrazee/deadlines')
lines.append('REFRESH-INTERVAL;VALUE=DURATION:PT1H')
lines.append('X-PUBLISHED-TTL:PT1H')

now_stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

for i, item in enumerate(upcoming):
    # Parse date with offset (e.g. -04:00 or +05:30)
    dt = datetime.fromisoformat(item['date'])
    utc = dt.astimezone(timezone.utc)
    end_utc = utc + timedelta(minutes=15)
    
    dtstart = utc.strftime('%Y%m%dT%H%M%SZ')
    dtend = end_utc.strftime('%Y%m%dT%H%M%SZ')
    
    summary = f"{course_names[item['course']]}: {item['label']}"
    desc = item['note'] if item['note'] else f"{course_names[item['course']]} deadline"
    uid = f"krish-{item['course']}-{i}-{dtstart}@deadlines.krish"
    
    lines.append('BEGIN:VEVENT')
    lines.append(f'UID:{uid}')
    lines.append(f'DTSTAMP:{now_stamp}')
    lines.append(f'DTSTART:{dtstart}')
    lines.append(f'DTEND:{dtend}')
    lines.append(f'SUMMARY:{summary}')
    lines.append(f'DESCRIPTION:{desc}')
    # 1 day before
    lines.append('BEGIN:VALARM')
    lines.append('TRIGGER:-P1D')
    lines.append('ACTION:DISPLAY')
    lines.append(f'DESCRIPTION:Tomorrow: {summary}')
    lines.append('END:VALARM')
    # 1 hour before
    lines.append('BEGIN:VALARM')
    lines.append('TRIGGER:-PT1H')
    lines.append('ACTION:DISPLAY')
    lines.append(f'DESCRIPTION:In 1 hour: {summary}')
    lines.append('END:VALARM')
    lines.append('END:VEVENT')

lines.append('END:VCALENDAR')

with open('/sessions/vigilant-magical-carson/mnt/outputs/deadlines-site/deadlines.ics', 'w') as f:
    f.write('\r\n'.join(lines) + '\r\n')

print(f"Generated {len(upcoming)} events in deadlines.ics")
