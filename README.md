Automatic addding scan targets to WVS prior to lastest version 14

Please change to your wvs mgmt url in script "https://acunetix_url:3443"

- 1 Add urls to file'wvs_url.xls'
(Just one column with url)

usage:
- 2 Edit wvs_auto_scan.py and replace to your credentials
u = 'demo@demo.com'
p = 'pa$$word123'

- 2.1 Replace all "acunetix_url" to your acunetix real url
- 2.2 Change if needed
scanid='11111111-1111-1111-1111-111111111111'#default scan id   11111111-1111-1111-1111-111111111111

```python3 wvs_auto_scan.py```
