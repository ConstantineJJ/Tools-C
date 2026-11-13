"""Pure project-review identities and bounded JSON/path helpers; no engine imports."""
import hashlib
import json
import re
from validation_core import Violation, identifier, local_path, require

PACKET_LIMIT = 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def key(value):
    identifier(value)
    require(len(value) <= 128, 'Identifier budget exceeded', 'E_LIMIT')


def path_in(root, value):
    require(isinstance(value, str) and len(value) <= 4096, 'Path budget exceeded', 'E_LIMIT')
    return local_path(root, value)


def strict_json(raw):
    # check.read_json reads a whole file; decode our already bounded bytes instead.
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, 'Duplicate JSON key', 'E_JSON')
            result[key] = value
        return result

    def nonfinite(value):
        raise Violation('E_JSON', 'Non-finite JSON value')

    def finite(value):
        result = float(value)
        require(result not in (float('inf'), float('-inf')), 'Non-finite JSON number', 'E_JSON')
        return result

    try:
        return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs,
                          parse_constant=nonfinite, parse_float=finite)
    except (UnicodeError, ValueError, RecursionError) as error:
        raise Violation('E_JSON', 'Invalid bounded UTF-8 JSON') from error


def refs(values):
    require(isinstance(values, list) and all(isinstance(x, str) for x in values), 'Expected ID array')
    require(len(values) == len(set(values)), 'Duplicate reference', 'E_ID')
    for value in values:
        key(value)
    return values


def hash_value(value):
    require(isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value), 'Invalid SHA-256')


