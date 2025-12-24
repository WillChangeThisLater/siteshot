# siteshot
[llm](https://www.github.com/simonw/llm) fragment for taking screenshots of a site


## installation
```bash
git clone https://github.com/WillChangeThisLater/siteshot
cd siteshot
llm install -e .
```

## usage
```bash
llm -f siteshot:https://news.ycombinator.com/ "extract the top 5 links from this site"
Here are the top 5 links from the provided Hacker News page:

1. [A Fabrice Bellard Releases MicroQuickJS](https://github.com/bellard) - 852 points
2. [X-ray: a Python library for finding bad redactions in PDF documents](https://github.com/freelawproject) - 206 points
3. [Unifi Travel Router](https://u.com) - 113 points
4. [A Texas app store verification law blocked by federal judge](https://macrumors.com) - 163 points
5. [Some Epstein file redactions are being undone with hacks](https://theguardian.com) - 202 points
```
