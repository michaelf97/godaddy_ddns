# godaddy_ddns
Python software that can update A records for domains held by GoDaddy.com.

## How to use
```py
DynamicDns(
  key=<key>,
  secret=<secret>,
  domain="mydomain.com",
  exclusions=["subdomain1", "subdomain2"]
)
```
