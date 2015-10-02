# ph

### Usage

```
$ ph "+1 (415) 922-5555" -c "US"
{
  "alpha2": "US",
  "country_code": 1,
  "errors": [
    "invalid country code or region"
  ],
  "is_valid": false,
  "name": "United States",
  "official_name": "United States of America",
  "phone_str": "+1(415)922-5555",
  "phone_str_digits_only": "+14159225555",
  "raw_input": "+1 (415) 922-5555"
}
```
