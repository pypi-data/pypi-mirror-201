# Schema Keys

## Generic Keys
Inherits all keys from 'generic'

## String Specific Keys
```yaml
type: 'string'

reference: { unique options }

minimum: <int | default -> 0 > # >= 0
# Minimum required string length

maximum: < int > # >= 0
# Maximum allowed string length

allowed_values:
- < string >
# List of strings
# Dependis on 'regex_mode':
# == false: String must be equal to any string in the list.
# == true: String must match with any regex in the list.

not_allowed_values:
- < string >
# List of strings
# Dependis on 'regex_mode':
# == false: String mustn't be equal to any string in the list.
# == true: String mustn't match with any regex in the list.

regex_mode: < bool | default -> false >
# Use strings in 'allowed_values' and 'not_allowed_values' for regex matching.

regex_multiline: < bool | default -> false >
# Use multiline matching for regex tests or not

regex_fullmatch: < bool | default -> true >
# String must fully match.
```