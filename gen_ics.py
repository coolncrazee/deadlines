#!/usr/bin/env python3
"""Generate two ICS calendar feeds from index.html:
   - deadlines.ics  — course deadlines (with 1 day + 1 hour alarms)
   - study.ics      — daily 1hr study sessions (with 15 min alarm)
"""
from datetime import datetime, timedelta, timezone
import re

with open('/sessions/vigilant-magical-carson/mnt/outputs/deadlines-site/index.html') as f:
    html = f.read()

m = re.search(r'const deadlines = \[(.*?)\n\];', html, re.DOTALL)
arr_text = m.group(1)

items = []
for line in arr_text.split('\n'):
    if 'date:' not in line or 'course:' not in line:
        continue
    course_m = re.search(r"course:\s*'([^']+)'", line)
    label_m = re.search(r"label:\s*'([^']+)'", line)
    date_m = re.search(r"date:\s*'([^']+)'", line)
    if not (course_m and label_m and date_m):
        continue
    item = {
        'course': course_m.group(1),
        'label': label_m.group(1),
        'date': date_m.group(1),
        'done': 'done: true' in line,
        'is_study': "type: 'study'" in line,
    }
    note_m = re.search(r"note:\s*'([^']+)'", line)
    item['note'] = note_m.group(1) if note_m else ''
    items.append(item)

course_names = {'cs': 'CS 231', 'afm': 'AFM 231', 'math': 'CO 380', 'goals': 'Goal'}

def build_ics(items, cal_name, cal_desc, alarms):
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Krish//Spring 2026//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        f'X-WR-CALNAME:{cal_name}',
        f'X-WR-CALDESC:{cal_desc}',
        'REFRESH-INTERVAL;VALUE=DURATION:PT1H',
        'X-PUBLISHED-TTL:PT1H',
    ]
    now_stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

    for i, item in enumerate(items):
        if item['done']:
            continue
        dt = datetime.fromisoformat(item['date'])
        utc = dt.astimezone(timezone.utc)
        end_utc = utc + timedelta(minutes=60 if item['is_study'] else 15)

        summary = f"{'📚 ' if item['is_study'] else ''}{course_names[item['course']]}: {item['label']}"
        desc = item['note'] if item['note'] else f"{course_names[item['course']]} {'study session' if item['is_study'] else 'deadline'}"
        kind = 'study' if item['is_study'] else 'dl'
        uid = f"krish-{kind}-{item['course']}-{i}-{utc.strftime('%Y%m%dT%H%M%SZ')}@deadlines.krish"

        lines += [
            'BEGIN:VEVENT',
            f'UID:{uid}',
            f'DTSTAMP:{now_stamp}',
            f'DTSTART:{utc.strftime("%Y%m%dT%H%M%SZ")}',
            f'DTEND:{end_utc.strftime("%Y%m%dT%H%M%SZ")}',
            f'SUMMARY:{summary}',
            f'DESCRIPTION:{desc}',
        ]
        for trigger, label_prefix in alarms:
            lines += [
                'BEGIN:VALARM',
                f'TRIGGER:{trigger}',
                'ACTION:DISPLAY',
                f'DESCRIPTION:{label_prefix} {summary}',
                'END:VALARM',
            ]
        lines.append('END:VEVENT')

    lines.append('END:VCALENDAR')
    return '\r\n'.join(lines) + '\r\n'

deadline_items = [it for it in items if not it['is_study']]
study_items = [it for it in items if it['is_study']]

with open('/sessions/vigilant-magical-carson/mnt/outputs/deadlines-site/deadlines.ics', 'w') as f:
    f.write(build_ics(
        deadline_items,
        'Krish — Spring 2026 Deadlines',
        'Course deadlines (auto-updated)',
        [('-P1D', 'Tomorrow:'), ('-PT1H', 'In 1 hour:')]
    ))

with open('/sessions/vigilant-magical-carson/mnt/outputs/deadlines-site/study.ics', 'w') as f:
    f.write(build_ics(
        study_items,
        'Krish — Spring 2026 Study Plan',
        '1hr daily study sessions (auto-updated)',
        [('-PT15M', 'Starts in 15 min:')]
    ))

dl_active = sum(1 for it in deadline_items if not it['done'])
st_active = sum(1 for it in study_items if not it['done'])
print(f"deadlines.ics: {dl_active} events  ·  study.ics: {st_active} events")
