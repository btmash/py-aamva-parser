from __future__ import annotations

import re


class Regex:
    def first_match(self, pattern: str, data: str) -> str | None:
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
            match = compiled.search(data)
            if not match or len(match.groups()) < 1:
                return None
            matched = match.group(1).strip()
            return matched if matched else None
        except re.error:
            return None
