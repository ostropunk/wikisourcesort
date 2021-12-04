# wikisourcesort
 A script for sorting references and sources on wikipedia

This script was created for sorting reference tags on wikipedia. You need to copy the wikitext from the article to a txt-file and place that in the same folder as the script. Once you run the script it will create a new txt-file where it has replaced existing references with reference tags and inserted a list with all the references at the bottom of the article.

**Warning!** This will remove any formating or text between the `<ref></ref>`-tags except URL:s and also does not work with references that do not contain any URL:s, this is partly by design as it forces the user to check if the URL:s work.


The script turns this:
>`Festivalen öppnade med ''[[My Blueberry Nights]]'', regisserad av [[Wong Kar-wai]] <ref>{{Tidningsref|url=https://www.nytimes.com/2007/05/18/movies/18cann.html}}</ref> och avslutades med ''Days of Darkness (L'Âge des ténèbres)'' av [[Denys Arcand]] . <ref>{{Tidningsref|url=http://www.cbc.ca/news/arts/quebec-filmmaker-arcand-closes-cannes-on-comedic-note-1.672613}}</ref> [[Diane Kruger]] var konferencier.<ref>{{Tidningsref|url=http://www.festival-cannes.com/en/article/49781.html}}</ref>`
>`== Referenser ==`
>`<references/>`

Into this:

>`Festivalen öppnade med ''[[My Blueberry Nights]]'', regisserad av [[Wong Kar-wai]]<ref name="nytimes.com.1" /> och avslutades med ''Days of Darkness (L'Âge des ténèbres)'' av [[Denys Arcand]].<ref name="cbc.ca.1" /> [[Diane Kruger]] var konferencier.<ref name="festival-cannes.com.1" />`

>`== Referenser ==`
>`<references>`
>`<ref name="nytimes.com.1">https://www.nytimes.com/2007/05/18/movies/18cann.html</ref>`
>`<ref name="cbc.ca.1">https://www.cbc.ca/news/entertainment/quebec-filmmaker-arcand-closes-cannes-on-comedic-note-1.672613|tidning=CBC|hämtdatum=2021-11-27</ref>`
>`<ref name="festival-cannes.com.1">http://www.festival-cannes.com/en/article/49781.html</ref>`
>`</references>`