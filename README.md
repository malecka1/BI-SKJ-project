# BI-SKJ project (Czech README)


### Zadání

  Úkolem semestrální práce je vytvořit skript, který ze zadaných vstupních dat (uložených v souboru/souborech nebo na webu (stačí schéma http)) vytvoří animaci grafu (jako výstupní formát jsem zvolil GIF) pomocí Gnuplotu. Pro jednu sadu vstupních souborů se předpokládá 1 výsledná animace. Pokud je zadáno více vstupních souborů, uvažují se dvě situace:  
  1) časové intervaly jednotlivých souborů se nepřekrývají -> spojení datových souborů podle uvedených časů, kreslí se jeden graf (jako by byl zadán jeden soubor)  
  2) časové intervaly jednotlivých souborů se překrývají -> kreslí se pro každé překrývající se soubory samostatné křivky  
  Skript je možné parametrizovat pomocí přepínačů a pomocí konfiguračního souboru (i současně, přepínače na příkazové řádce mají přednost).
  
  ![SKJ2](http://hockey.maweb.eu/other/githubSKJ2.gif)  
  ![SKJ3](http://hockey.maweb.eu/other/githubSKJ3.gif)  

### Specifikace přepínačů [přepínač : direktiva : popis]

  -t : TimeFormat : timestamp formát, program podporuje přepínače %{YymdHMS}, výchozí hodnota "[%Y-%m-%d %H:%M:%S]"  
  -X : Xmax : x-max, nabývá hodnot {auto, max, konkrétní timestamp hodnota}, výchozí hodnota "max", volitelný přepínač  
  -x : Xmin : x-min, nabývá hodnot {auto, min, konkrétní timestamp hodnota}, výchozí hodnota "min", volitelný přepínač  
  -Y : Ymax : y-max, nabývá hodnot {auto, max, konkrétní int/float hodnota}, výchozí hodnota "auto"  
  -y : Ymin : y-min, nabývá hodnot {auto, min, konkrétní int/float hodnota}, výchozí hodnota "auto"  
  -S : Speed : rychlost animace, hodnota int/float, výchozí hodnota "1"  
  -T : Time : doba vykreslování animace, hodnota int/float  
  -F : FPS : FPS, výchozí hodnota "25"  
  -c : CriticalValue : mezní hodnoty, subhodnoty odděleny znakem ":", subhodnota "[xy]=int/float", povoleno více výskytů, volitelný přepínač  
-l : Legend : název grafu  
-g : GnuplotParams : efekty pro Gnuplot, hodnota "Gnuplot parametr", povoleno více výskytů  
-e : EffectParams : efekt animace, v mé implementaci povolen jeden výskyt nabývající hodnotu nezáporného celého čísla vyjadřujícího délku animace (počet bodů postupného vykreslování), výchozí hodnota "0" znamená žádnou animaci  
  -f : n/a : konfigurační soubor, hodnota "pathname"  
  -n : Name : název složky pro výstupní animaci, výchozí hodnota je název skriptu, pokud již adresář existuje, název adresáře bude končit na "_i", kde i=max(i,0)+1


### Syntaxe

    $ ./malecka1 [-přepínače] soubor|url...

  Zobrazení nápovědy

    $ ./malecka1 -h, případně --help


### Testy

  K semestrální práci je přibalen jednoduchý skript "tests.py", jehož spuštěním se provede přes 30 testů, první část z nich ověřuje především mezní hodnoty, druhá část používá především validní vstupní data ze složky "data" a vytvoří několik animací, které pokrývají různé kombinace všech možností skriptu. Volání a případný chybový výstup každého testu se pro přehlednost uloží do souboru "output.txt".

  Spuštění testovacího skriptu:

    $ ./tests.py


### Licence
  
  Více v souboru *LICENSE*.


### Developed By

  Maleček Kamil, 2015
