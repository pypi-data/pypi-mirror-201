# HTML for NLP

## Installation

```bash
pip install git+https://github.com/druskacik/html_for_nlp
```

## Usage

```python

import requests
from html_for_nlp import HTMLDocument

r = requests.get('https://google.com')

doc = HTMLDocument(r.content)

print(doc.full_text)
```

Output:

```
<[document]>
Google
Vyhľadávanie
<a>
Obrázky
</a>
<a>
Mapy
</a>
<a>
Play
</a>
<a>
YouTube
</a>
<a>
Správy
</a>
<a>
Gmail
</a>
<a>
Disk
</a>
<a>
Ďalšie
»
</a>
<a>
História hľadania
</a>
|
<a>
Nastavenia
</a>
|
<a>
Prihlásiť sa
</a>
<a>
Rozšírené vyhľadávanie
</a>
<span>
<a>
Reklama
</a>
<a>
Riešenia pre firmy
</a>
<a>
Všetko o Google
</a>
<a>
Google.sk
</a>
<p>
© 2023
</p>
</span>
</[document]>
```