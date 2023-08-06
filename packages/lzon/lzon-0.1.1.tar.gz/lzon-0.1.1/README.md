# LZON (Lazy JSON)

Sometimes, an API may not provide the response as a fully developed JSON object. Certain keys might need to be reparsed as JSON before you can then continue to index it. LZON should help with this. You index, and it only parses when it's relevant.

## Example

```py
import lzon

response = r"""
{
    "bumble": "{\"bee\": [1, 2, 64]}"
}
"""

data = lzon.loads(response)
print(data['bumble']['bee'][2])  # Should return 64
```