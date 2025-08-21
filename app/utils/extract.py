import re
import json

# Filter the Output from the Model

def extract_recommendation(text: str):
    items = []
    for ln in text.splitlines():
        m = re.match(r'^\s*(?:[-*]|\d+[\.\)])\s*(.+?)\s*$', ln)
        if m:
            item = re.sub(r'[，。,;：:]\s*$', '', m.group(1).strip())
            items.append(item)
    return items if items else ["There is no suitable place nearby"]

def _json_chunks(s: str):
    depth, start = 0, None
    for i, ch in enumerate(s):
        if ch == '{':
            if depth == 0: start = i
            depth += 1
        elif ch == '}':
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    yield s[start:i+1]
                    start = None

def extract_schedule(text_or_obj):
    if isinstance(text_or_obj, dict):
        return text_or_obj

    if not isinstance(text_or_obj, str):
        return {"Morning": [], "Afternoon": [], "Evening": []}

    for chunk in _json_chunks(text_or_obj):
        try:
            obj = json.loads(chunk)
            if all(k in obj for k in ("Morning", "Afternoon", "Evening")):
                return obj
        except json.JSONDecodeError:
            continue
    return {"Morning": [], "Afternoon": [], "Evening": []}
