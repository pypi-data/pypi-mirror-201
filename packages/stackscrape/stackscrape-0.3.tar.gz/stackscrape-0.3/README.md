Get questions and answers from Stack Overflow that match some criteria 
(tags or title text).

```
Usage:
  stackscrape [-s SITE] [-t TAG] [-f TEXT] [-d DAYS] [-n NUM] [-o OUT]
  stackscrape -h | --help
  stackscrape --version

Get questions and accepted answers from a StackExchange site.

Options:
  -s SITE --site=SITE     Which StackExchange site to query. [default: stackoverflow]
  -t TAG --tag=TAG        Fetch questions tagged with the given TAG.
  -f TEXT --filter=TEXT   Fetch questions containing the given TEXT in the their title.
  -d DAYS --days=DAYS     How many days back to go. [default: 365]
  -n NUM --num=NUM        Max number of items to fetch. [default: 1000]
  -o OUT --out=OUT        Save results to file OUT.
  -h --help               Show this screen.
  --version               Show version.
  
```
