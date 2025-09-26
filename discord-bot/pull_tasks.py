import json
import math
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date, datetime, timezone
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import requests

# ================== XML payloads ==================
REPORT_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<c:calendar-query xmlns:c="urn:ietf:params:xml:ns:caldav" xmlns:d="DAV:">
  <d:prop>
    <d:getetag/>
    <c:calendar-data/>
  </d:prop>
  <c:filter>
    <c:comp-filter name="VCALENDAR">
      <c:comp-filter name="VTODO"/>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>
"""

PROPFIND_BODY = """<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:prop>
    <d:displayname/>
    <d:resourcetype/>
    <c:supported-calendar-component-set/>
  </d:prop>
</d:propfind>
"""

NS = {"d": "DAV:", "c": "urn:ietf:params:xml:ns:caldav"}


def get_config(account: str) -> tuple[str, str, tuple[str, str]]:
    with open("/home/racer/solarcloud_config.json", "r") as conf:
        config = json.load(conf)
        account = account.lower()
        if account == "admin":
            USERNAME = config["USER"]
            PASSWORD = config["PASS"]
        elif account == "software":
            USERNAME = config["SOFTWARE_USER"]
            PASSWORD = config["SOFTWARE_PASS"]
        elif account == "electrical":
            USERNAME = config["ELECTRICAL_USER"]
            PASSWORD = config["ELECTRICAL_PASS"]
        elif account == "mech":
            USERNAME = config["MECH_USER"]
            PASSWORD = config["MECH_PASS"]
        NEXTCLOUD_URL = config["NEXTCLOUD_URL"].rstrip("/")
        CALDAV_HOME = (
            f"{config['CALDAV_PATH'].lstrip('/')}".rstrip("/") + f"/{USERNAME}/"
        )
        AUTH = (USERNAME, PASSWORD)
    return (NEXTCLOUD_URL, CALDAV_HOME, AUTH)


# ================== iCal helpers ==================
def unfold_ical(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        if line.startswith((" ", "\t")) and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def parse_prop(line: str):
    if ":" not in line:
        return line.upper(), {}, ""
    head, value = line.split(":", 1)
    parts = head.split(";")
    name = parts[0].upper()
    params = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            params[k.upper()] = v
        else:
            params[p.upper()] = ""
    return name, params, value


def parse_vtodos(ical_text: str):
    lines = unfold_ical(ical_text.strip())
    tasks = []
    task = None
    for line in lines:
        name, params, value = parse_prop(line)

        if name == "BEGIN" and value.upper() == "VTODO":
            task = {
                "SUMMARY": None,
                "UID": None,
                "DUE": None,
                "DESCRIPTION": None,
                "STATUS": None,
                "COMPLETED": None,
                "_PARENT_UID": None,  # if this task is a child
                "_CHILD_UIDS": [],  # if this task declares children (rare)
            }
            continue

        if name == "END" and value.upper() == "VTODO":
            if task and task.get("UID"):
                tasks.append(task)
            task = None
            continue

        if task is None:
            continue  # ignore VCALENDAR-level props

        if name in {"SUMMARY", "UID", "DUE", "DESCRIPTION", "STATUS", "COMPLETED"}:
            if task.get(name) is None:
                task[name] = value

        elif name == "RELATED-TO":
            reltype = params.get("RELTYPE", "").upper()
            if reltype in ("", "PARENT"):
                # Many servers omit RELTYPE; treat as PARENT by default
                task["_PARENT_UID"] = value
            elif reltype == "CHILD":
                task["_CHILD_UIDS"].append(value)

        if name == "DUE":
            # Save raw value (first seen) and params (for TZID/DATE handling)
            if task.get("DUE") is None:
                task["DUE"] = value
                task["_DUE_PARAMS"] = (
                    params  # NEW: keep ICS params like TZID, VALUE=DATE
                )

    return tasks


# ================== CalDAV helpers ==================
def calendars_with_vtodo(base_url: str, home_path: str, auth):
    url = urljoin(base_url + "/", home_path.lstrip("/"))
    headers = {"Depth": "1", "Content-Type": "application/xml; charset=utf-8"}
    r = requests.request(
        "PROPFIND", url, auth=auth, headers=headers, data=PROPFIND_BODY
    )
    if r.status_code != 207:
        raise RuntimeError(f"Calendar discovery failed: {r.status_code} {r.text}")

    root = ET.fromstring(r.content)
    out = []
    for resp in root.findall("d:response", NS):
        href_el = resp.find("d:href", NS)
        if href_el is None:
            continue
        href = href_el.text

        # Must be a calendar collection
        rtype = resp.find(".//d:resourcetype", NS)
        if rtype is None or rtype.find("c:calendar", NS) is None:
            continue

        # Prefer calendars that declare VTODO support; if compset missing, include anyway
        compset = resp.find(".//c:supported-calendar-component-set", NS)
        include = True
        if compset is not None:
            names = {
                (comp.get("name") or "").upper()
                for comp in compset.findall("c:comp", NS)
            }
            include = "VTODO" in names

        if not include:
            continue

        name_el = resp.find(".//d:displayname", NS)
        displayname = (
            name_el.text if name_el is not None else href.rstrip("/").split("/")[-1]
        )
        out.append((href, displayname))
    return out


def report_vtodos(base_url: str, cal_href: str, auth):
    url = urljoin(base_url + "/", cal_href.lstrip("/"))
    headers = {"Depth": "1", "Content-Type": "application/xml; charset=utf-8"}
    r = requests.request("REPORT", url, auth=auth, headers=headers, data=REPORT_BODY)
    if r.status_code != 207:
        raise RuntimeError(f"REPORT failed for {url}: {r.status_code} {r.text}")

    root = ET.fromstring(r.content)
    found = []
    for resp in root.findall("d:response", NS):
        href_el = resp.find("d:href", NS)
        cdata_el = resp.find(".//c:calendar-data", NS)
        if href_el is None or cdata_el is None or not cdata_el.text:
            continue
        href = href_el.text
        for vt in parse_vtodos(cdata_el.text):
            vt["href"] = href
            found.append(vt)
    return found


# ================== Printing: grouped by List ==================
def _print_single_grouped(
    uid, by_uid, children_local, listname_of_uid, allowed_uids, indent, seen
):
    if uid in seen:
        return
    seen.add(uid)
    t = by_uid.get(uid)
    if not t:
        return
    pad = "  " * indent
    print(f"{pad}Task: {t.get('SUMMARY') or '(no summary)'}")
    # List header is printed outside; show cross-list parent info if relevant
    parent_uid = t.get("_PARENT_UID")
    if parent_uid and parent_uid not in allowed_uids and indent == 0:
        parent = by_uid.get(parent_uid)
        parent_name = (parent.get("SUMMARY") if parent else None) or parent_uid
        parent_list = listname_of_uid.get(parent_uid, "(unknown list)")
        print(f"{pad}(Subtask of: {parent_name} — {parent_list})")
    if t.get("DUE"):
        print(f"{pad}Due: {t['DUE']}")
    if t.get("STATUS"):
        print(f"{pad}Status: {t['STATUS']}")
    print(f"{pad}UID: {t.get('UID')}")
    print(f"{pad}Link path: {t.get('href')}")
    if t.get("DESCRIPTION"):
        print(f"{pad}Notes: {t['DESCRIPTION']}")
    print()

    for child_uid in children_local.get(uid, []):
        _print_single_grouped(
            child_uid,
            by_uid,
            children_local,
            listname_of_uid,
            allowed_uids,
            indent + 1,
            seen,
        )


def print_grouped_by_list(by_uid, children_of, listname_of_uid):
    # Build list -> [uids]
    lists = defaultdict(list)
    for uid, t in by_uid.items():
        lists[listname_of_uid.get(uid, "(unknown)")].append(uid)

    for list_name in sorted(lists.keys()):
        uids = lists[list_name]
        allowed = set(uids)

        # Children map restricted to this list (no cross-list recursion)
        children_local = {}
        for parent in uids:
            kids = [c for c in children_of.get(parent, []) if c in allowed]
            if kids:
                children_local[parent] = kids

        local_children = {c for cs in children_local.values() for c in cs}
        roots_in_list = [u for u in uids if u not in local_children]

        print(f"=== List: {list_name} ===")
        seen = set()
        for uid in roots_in_list:
            _print_single_grouped(
                uid,
                by_uid,
                children_local,
                listname_of_uid,
                allowed,
                indent=0,
                seen=seen,
            )
        print()  # spacer between lists


def ical_unescape(text: str | None) -> str | None:
    if text is None:
        return None
    return (
        text.replace("\\\\", "\\")
        .replace("\\n", "\n")
        .replace("\\N", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
    )


def parse_due(
    due_value: str | None, due_params: dict | None, default_tz: str = "America/New_York"
):
    if not due_value:
        return None, False

    params = {k.upper(): v for k, v in (due_params or {}).items()}
    try:
        # Case 1: explicit VALUE=DATE or looks like YYYYMMDD
        if params.get("VALUE", "").upper() == "DATE" or (
            len(due_value) == 8 and due_value.isdigit()
        ):
            y = int(due_value[0:4])
            m = int(due_value[4:6])
            d = int(due_value[6:8])
            return date(y, m, d), True

        # Case 2: UTC date-time ending with Z
        if due_value.endswith("Z"):
            dt = datetime.strptime(due_value, "%Y%m%dT%H%M%SZ").replace(
                tzinfo=timezone.utc
            )
            return dt, False

        # Case 3: TZID param
        tzid = params.get("TZID")
        if tzid:
            dt = datetime.strptime(due_value, "%Y%m%dT%H%M%S")
            return dt.replace(tzinfo=ZoneInfo(tzid)), False

        # Case 4: naive → assume default_tz
        dt = datetime.strptime(due_value, "%Y%m%dT%H%M%S")
        return dt.replace(tzinfo=ZoneInfo(default_tz)), False

    except Exception:
        # If parsing fails, just skip fancy formatting
        return None, False


def humanize_due(parsed, is_date_only: bool, display_tz: str = "America/New_York"):
    if parsed is None:
        return None

    now = datetime.now(ZoneInfo(display_tz))

    if is_date_only:
        # Show as local date; add relative days
        due_dt = datetime(
            parsed.year, parsed.month, parsed.day, 0, 0, tzinfo=ZoneInfo(display_tz)
        )
    else:
        # Convert to display tz
        due_dt = parsed.astimezone(ZoneInfo(display_tz))

    # Relative chunk (very compact)
    delta = due_dt - now
    secs = int(delta.total_seconds())
    sign = "-" if secs < 0 else ""
    secs = abs(secs)
    days = secs // 86400
    hours = (secs % 86400) // 3600
    rel = f"{sign}{days}d{hours}h" if days else f"{sign}{hours}h"

    # Format absolute
    if is_date_only:
        abs_str = due_dt.strftime("%a, %b %d, %Y")
    else:
        abs_str = due_dt.strftime("%a, %b %d, %Y %I:%M %p %Z")

    return f"{abs_str} ({'overdue' if sign=='-' else 'in'} {rel.lstrip('-')})"


def clamp(text: str | None, limit: int) -> str | None:
    if text is None:
        return None
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "…"


def chunked(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


# ================== Main ==================
def main():
    try:
        calendars = calendars_with_vtodo(NEXTCLOUD_URL, CALDAV_HOME, AUTH)
        if not calendars:
            print("No task lists (VTODO calendars) found.")
            return

        all_tasks = []
        by_uid = {}
        listname_of_uid = {}
        list_href_of_uid = {}

        for cal_href, cal_name in calendars:
            vtodos = report_vtodos(NEXTCLOUD_URL, cal_href, AUTH)
            for t in vtodos:
                if not t.get("UID"):
                    continue
                # Attach list metadata
                t["_LISTNAME"] = cal_name
                t["_LISTHREF"] = cal_href
                by_uid[t["UID"]] = t
                listname_of_uid[t["UID"]] = cal_name
                list_href_of_uid[t["UID"]] = cal_href
                all_tasks.append(t)

        # Build global parent → children (so we can see cross-list relationships)
        children_of = defaultdict(list)
        for t in all_tasks:
            if t.get("_PARENT_UID"):
                children_of[t["_PARENT_UID"]].append(t["UID"])
            for cu in t.get("_CHILD_UIDS", []):
                children_of[t["UID"]].append(cu)

        # Print grouped by list (with per-list trees)
        print_grouped_by_list(by_uid, children_of, listname_of_uid)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
