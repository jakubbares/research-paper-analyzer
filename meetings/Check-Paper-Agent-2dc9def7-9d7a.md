# Check Paper Agent

**Meeting Date:** 19th Jan, 2026 - 1:30 PM

---

**Jakub Bares** *[00:00]*: Jsi doma? 
**Jan Hůla** *[00:01]*: Na běžku se potřebuji, víš, na notebook. 
**Jakub Bares** *[00:04]*: Jo, jo, jsi doma? 
**Jan Hůla** *[00:06]*: Jo, jo. 
**Jakub Bares** *[00:07]*: Máš nějakou konferenci dneska, jo, nebo tato týden? 
**Jan Hůla** *[00:11]*: Jo, jo, já jsem tady mám, no. 
**Jakub Bares** *[00:13]*: Jo, jo. To. 
**Jan Hůla** *[00:26]*: U tebe, no, jo. 
**Jakub Bares** *[00:29]*: No, dělám na projektech pro WHO Zároveň teďka updatuju stránku na autismus.adhd Potom ještě dělám ten meetup, teďka v pondělí bude meetup příští týden. Což já organizuju no. Jo aha. Tam 130 lidí tam mám. Ty vrdil. A. 
**Jan Hůla** *[01:18]*: Na jaké to je téma? Je. 
**Jakub Bares** *[01:25]*: To skupina se jmenuje Prague AI Driven Software Meetup. A téma je Future of European Software in the Age of Large Language Models. Chci rozebrat ten manifest. Jsi ti pustil ten manifest, nebo ne? Myslím, že ne. Ty vole, já to taky zapomínám. Ty vole, já tě zapuštu do podseku. Jo. 
**Jan Hůla** *[01:53]*: Jo, jo. 
**Jakub Bares** *[01:56]*: Jsem napisal manifest na téma, jak by měla fungovat agent-driven civilizace evropská a jaké máme výhody jako Evropa v této době, kdy jde o to se poučit ze historie a v podstatě nastavit ty věci správně, morálně a korektně. A tak je to takový dlouhatánský manifest a udělal jsem k tomu moje webovky, vlastně tyhle, co jsem někde poslal a snažím se tam nějak, možná kdyby se mi podařilo tam dát ČVU jako partnera, tak by to bylo fajn, k nevýkonnosti voslovit. No. 
**Jan Hůla** *[02:47]*: To já si myslím, že to bylo o hubu trošku. Já se můžu zeptat, jak to chodí, ale jako... Já se můžu zeptat, no. 
**Jakub Bares** *[03:05]*: To budeš hodnej, no. Já nevím, jak to... Jo. No. 
**Jan Hůla** *[03:12]*: Dobré, já ti můžu říct, co jsem vykoumal. Ještě. 
**Jakub Bares** *[03:18]*: K práci se mi podařilo udělat teda... Tímto názdílem teďka rychle. Jo. Tak jenom jako, ať tě pak ukážu, já jsem vždycky vyskoušet mě poslal repo, já jsem ho udělal tentokrát veřejný, nevím, mně jako přišlo, že to jedno. Ehm, a, ehm, prostě funguje to takhle, že tady máš jako má upload. A potom prostě pustíš analýzu. A pak vlastně ono to jako pustí pro tu danou věc, kterou jako zjištíš, ti to pustí analýzu. Mhm. A je tady těch věcí prostě miliarda těch promptů je hrzný kotel, který všechny věci se dají vyextrahovat. Možná to uděláme jako tlačítka, než tady ten slide a takhle, no. Taký pomalý, nevím, přece jak pomalý, ale prostě vyextrahuje to ty věci, no. 
**Jan Hůla** *[04:19]*: Takže tady máš zkrátka, jak to funguje v pozadí? Co se děje v pozadí? Ten paper se převede na Markdown nebo? Na. 
**Jakub Bares** *[04:32]*: Co? Jak. 
**Jan Hůla** *[04:33]*: To funguje teď v pozadí? Co se tam děje? Jak tam nahráš ten paper? 
**Jakub Bares** *[04:39]*: Jo, myslím, že se to převádí na Markdown a pak se to z toho extrahuje z toho BDF kanálu. Já. 
**Jan Hůla** *[05:18]*: Jsem si myslel, že... Že vlastně uděláme něco, co nám bude jako interaktivně, jako ta úplně ideální seta byl takový, že ty vlastně máš nějaké query, jo, ty tam dáš ten paper, nebo nejenom jeden paper, ale dál jsi tam sadu paperů. Ty dál jsi tam třeba, dál jsi paperů na jednou a teďka máš třeba query, řekneš, jaké typy contributionů se v těch paperech vyskytují a chci vidět vlastně, jako u každého contributionů, chci vidět, Jako nějak zaspecifikuješ, co u každého contributionu chceš. A ten systém by ti vygeneroval UI, které by ti tohleto tvojí query zobrazovalo. Jo. 
**Jakub Bares** *[06:10]*: Jasně, to je tady ta věc ještě. 
**Jan Hůla** *[06:14]*: Že jedna může být třeba typy contributionů, druhá může být, ukáž mi všechny experimenty, které v tom paperu jsou a chci to mít zobrazené tak, že budu mít vždycky název paperů a pod tím budou ty experimenty a u každého experimentu bude, jaké tam jsou benchmarky a nějak vlastně jako zadefinuješ, co chceš a ten systém, za prvé ti to vysaje z toho, z těch paperů a pak to zvizualizuje nějak jako přímo na míru pro tu query. Jo. 
**Jakub Bares** *[06:44]*: Jo, jo. Jo. 
**Jan Hůla** *[06:47]*: To byla... To byla ta myšlenka, že by si to... Jasný. 
**Jakub Bares** *[06:54]*: Jasný, jasný. OK. Hele, já myslím, že to bude dobré, je tam mít tyhle prompty na pozadí, to já myslím, že je dobré, protože... Jakoby, já si myslím, že by to mělo fungovat nějak. Já bych to udělal tak, že bych to si udělal jako... Ty extractory bych nechal takhle, jak jsou. Teďka. 
**Jan Hůla** *[07:26]*: To máš tak, že máš několik extractorů, každý extractor je daný jedným promptem, jo? Jasně. 
**Jakub Bares** *[07:32]*: A. 
**Jan Hůla** *[07:32]*: Oni ti vlastně vytáhujou konkrétní specifické věci. Takže vidím, že tam máš jako... Jakože třeba některé věci asi nedávají smysl. Asi vidět jako separátní rovnice, to ti asi nic moc neřekne. 
**Jakub Bares** *[07:57]*: Když. 
**Jan Hůla** *[07:59]*: Ukážeš, co tam teda ještě máš za sekce, tak tam máš Contributions, Experiment, to dává smysl, Architectures, Hyperparameters, Ablations, baselines, algorytms, limitations, future work. Jakože jo, tak mít tam sexy future work, to vlastně se můžeš z tom paperu nascrollovat na tu stránku a podívat si, co tam mají, že? 
**Jakub Bares** *[08:54]*: To bude mít jako jiný grále, když budeme dělat víc věcí najednou, že jo? Že co? To bude mít jako jiný grále, když budeme dělat víc paperů najednou, že prostě budeš mít jakobe... Jo. ...porovnání. To si myslím, že je určitě fajn. A teď je otázka, jak vlastně zobrazit to UI na míru. Jestli teda toho to sedí, že tady takovéhle věci by dávalo smysl extrahovat, nebo jestli to něco chybí za tebe? Já. 
**Jan Hůla** *[09:29]*: Ti možná ukážu, jak jsem to... Já. 
**Jakub Bares** *[09:31]*: Si myslím, že prostě by to možná dávalo smysl udělat, jakože jsi tam naklikáš, protože zase jako nechceš prostě úplně vymýšlet kolo. Zaběhu. 
**Jan Hůla** *[09:45]*: Myslí, jo? Jakože neseš zaběhu generovat? Když. 
**Jakub Bares** *[09:48]*: To budeš používat, tak se myslím, že by stačilo jako tam naklikat vlastně, co jako chceš zobrazit na tom dashboardu. Víš, že to je pohodlnější jako si uvědomit, co jim mám mít. Tohle, tohle, tohle, než to jako diktovat z hlavy, podle mě, nevím. Aspoň pro většinu uživatelů to určitě bude příjemnější. Pro tebe možná ne, protože ty víš, co chceš, ale... Takže tam naklikáš tyhle ty věci prostě a použiješ tady ten původní prompt, který mám v tom Extractoru, nějak ho zmodifikuješ. Vezmeš tu templateu toho promptu, nějak ho zmodifikuješ a vyjdeš z něj prostě. A potom vymyslíš, jak to nějak celý zobrzovat na jednou. A ten záměr tedy asi je, aby... Co je záměr? Proč zobrzováte equations a algorithms v jednom dashboardu? Jaký to má smysl? 
**Jan Hůla** *[10:51]*: Ty equations zrovna asi smysl nemají. Tam jde o to, Jakože některé věci možná nemají smysl vůbec jako takhle vizualizovat, ale třeba typy contributionů, ty máš jako sadu paperu a chtěl bych si získat nějaký high level přehled o tom, co v těch paperech je. Takže řekneš, ukáž mi všechny typy contributionů, u každého contributionu mi vypíšte tyhle informace Možná, že to zbytečně přiháníme a možná, že jsou nějaké třeba fixní počet queries, které bych se vždycky chtěl ptat. Možná, že ten počet těch queries není tak velký a možná, že to můžeme zafixovat a udělat to jenom na. 
**Jakub Bares** *[11:42]*: Jako mě se líbí ten myšlenka toho dynamického UI. Mně je to super nápad, jenom přemejšlen, v jakém smyslu to chceš provázat. V jakém smyslu tyhle jednotlivé atributy, jak je vůbec lze zobrazit dohromady. Jestli to vůbec jde nějak udělat. Jak. 
**Jan Hůla** *[12:05]*: Jsem to dělal já, tak já jsem si to Já jsem zkrátka měl query, já jsem mu dal ty, já jsem mu dal, já jsem vlastně to udělal tak, že já jsem mu udělal query, jedno, že jsem, pro jeden paper, jo, vytáhněni všechny, všechny contributiony z tohohle paperu, nějak mě pojmenují a tímhletím querym jsem projížděl, Všechny papery jsem s tím projel, vytáhl mi to nějaké strukturované informace už pro každý paper. A pak jsem mu řekl, zvizualizuj mi to do této moje stránky. A on si vymyslel způsob, jak mi to zvizualizovat. Na základě toho, že co věděl, co tam za informace má, tak si sám vymyslel způsob, jak mi to přihledně zobraznit. 
**Jan Hůla** *[13:08]*: A tam možná k té vizualizaci by tam mohly být nějaké instrukce, že třeba nikdy nedělej tady tohleto, nebo jako nějak se tam zarechinovalo nějaké obecné instrukce, jaké pravidla se mají používat při vytváření těch vizualizací, které on by musel dodržet. On by tam měl volnost, jak to udělá, ale měl by tam třeba nějaké instrukce, které by neporušil. Jasně. 
**Jakub Bares** *[13:39]*: Jasně, jasně. Dobře, já to můžu zkusit a předpokládám, že asi ideální format je, že ten dashboard má nějaké Reacty jako komponenty a do těch komponent já tam rvu nějaký HTML, ne? Jakože prostě ta stránka bude... Nech si úplně jako prostě, aby mi to zobrazilo úplně celou novou stránku z HTMLu. No. 
**Jan Hůla** *[14:05]*: Přesně tak. Můžete. 
**Jakub Bares** *[14:06]*: Si mít tu aplikaci, jak teďka je, a tam prostřebuje nějaký kanvás a tam se udělá ten dashboard. Jo. 
**Jan Hůla** *[14:14]*: Jo, přesně tak. Ale zatím bych to pak dal úplně minimalisticky, že nám bude stačit, že budeš mít nějaký template, který tam bude mít uprostřed nějaké právě místo, kde se vloží ta vygenerovaná vizualizace. Jo. 
**Jakub Bares** *[14:31]*: Já si myslím, že co by mohlo být cool, je použít tyhle všechny... Já si myslím, že fakt to není blbý vůbec mít tyhle různý Extractory. Jo. A myslím si, že co bylo cool, že řekneš chci teďka, jako lidským jazykem, popíš ten záměr, o co ti jako jde, že chceš prostě třeba udělat jako novéj paper na tohle téma a jde ti o to zjistit něco, jo? No. A ono to vlastně jako pochopí, OK, tak aby si tohle mohl udělat, tak potřebuješ tenhle ten, tenhle ten a tenhle ten extractor, kdy všechny ti jako semelu na ten paper, jo? Mhm. A pak vlastně teprve, jako by... Asi teda uděláme společnej extractor. Aby to nebežilo tři hodiny, tak prostě uděláš, že se ti ty extractory spojejí do jednoho extractoru, protože to se vejde do kontextu, nebo do odpovědi. A vlastně pro každý paper to uděláš zvlášť, asi pravděpodobně. 
**Jakub Bares** *[15:42]*: A potom... Protože jsou paralelně samozřejmě. Potom vlastně tyhle ty odpovědi teda hodíš do toho HTML generátoru a uvidíš ten výslek. Ale myslím si, že vlastně, aby opravdu to fungovalo nějak chytřejc, tak bude dobrý mít ty extractory definovaný, mít přesně definovaný, co se dá extrahovat, co se na tom dá extrahovat za atributy toho extractoru, A to by mohlo být jako dobrý, že by to prostě mělo nějakou štávní kulturu a nemuselo by to po každý vymejšat úplně znova. Otázka jestli tyto zrovna a ty extra, které jsou teďka tady, jsou ty správný, nebo nejsou. Contributions nevím teďka třeba, co to vlastně přesně ukazuje, jestli třeba, to asi bude to nejdůletější zrovna, takže tam možná by stačilo, to bylo důležité mít nějaký Ty. 
**Jan Hůla** *[16:45]*: To určitě chceš specifikovat, že jo? Určitě chceš být schopný říct, že třeba vyještřáli mi všechny contributions, které se týkají třeba učení. Jak to chceš být schopný toho zaběhu specifikovat? 
**Jakub Bares** *[17:05]*: Jo, jo. A ty contributions byly asi nejkreativnější. No. 
**Jan Hůla** *[17:18]*: Jo, nebo můžeš ti třeba zjistit ekstrávě všechny knihovny, které používají v experimentech. Jo. 
**Jakub Bares** *[17:27]*: Jo, jo. Nebo. 
**Jan Hůla** *[17:28]*: Jako celotka, nechceš to nějak omezovat se předem? A. 
**Jakub Bares** *[17:33]*: Zatím. 
**Jan Hůla** *[17:38]*: Pak vedme to tak, že to jsou židláme jako něco, co je pro naše interní použití. Vlastně ten vystup bude nějaká, že to může stránka zdávat s kriptem možná. Tak vlastně nemusíme se trápit tím, že to bude mít nějaké constrainty, kdyby to opravdu bylo někde na webu a mělo to... Takhle to může být hodně divoké. Když to někdy nevygeneruje správně, tak se nic neděje. 
**Jakub Bares** *[18:16]*: Dobře, dobře, tak jo, já se tam věřu na ty contributions hlavně udělám teda udělám teda nějaký custom extractor, který bude spojovat ty jiný extractory a doplnit tam, co tam chybí a druhá věc, co udělám je to UI na meadu Možná se. 
**Jan Hůla** *[18:45]*: I zeptej, já si myslím, že to už lidi dělají, že už od tom budou nějaké znalosti, jak vlastně ty dynamické UI dělat. Jo. 
**Jakub Bares** *[18:54]*: Já si myslím, že to není složitý. Vygenovat HTML je easy, tak prostě bude to statický HTML. Já to vnímám, že to bude statický, to je otázka, může to vždy být ten dynamický, nějakým JavaScriptem jednoduchým, Myslím si, že generovat reactive code to už je vyšší dívčí na míru. To si myslím, že není úplně dobrý nápad. Já se to vnímal tak, že vlastně co se třeba týče třeba toho prompt endu, jestli jsem ti o tom říkal, to jsem viděl na websamu z útejné startup, tak oni to podle mě dělají tak, že ti generujou čistě ty metadata, že ty komponenty už mají hotový. A vlastně generuje jenom jako metadata. A. 
**Jan Hůla** *[19:37]*: Jak se to jménoje? Promptend. V. 
**Jakub Bares** *[19:43]*: Ním vlastně dokážou se napojit na jakýkoliv data lajky a udělat z toho custom UI, že třeba potřebuješ změnit nějakou proměnou, dokonce potřebuješ zaměnit data. Aha. 
**Jan Hůla** *[19:57]*: Super, jo. Lidi. 
**Jakub Bares** *[19:59]*: Prostě udělají jako tabulku, kde prostě ten parametr změníš v kontextu toho všeho ostatního a ono se to samo uloží. Jo. 
**Jan Hůla** *[20:09]*: Jo, to je super, no. 
**Jakub Bares** *[20:13]*: Tak. 
**Jan Hůla** *[20:13]*: To je něco takového, co jsme uvažovali. Akorát. 
**Jakub Bares** *[20:18]*: Tam to je fakt, že to není zost tak kreativní a je to spíš jednoduché formuláře, jednoduché dashboardy, jednoduché grafy, nic služitýho a podle mě generují jenom ty backendový data a maximálně zvolej, co se zobrazí, ale je to parametrické. Není to, že by vymýšlelo nový vizualizace na on the fly, to určitě ne. Jo. 
**Jan Hůla** *[20:48]*: Jo. Jo, dobré. 
**Jakub Bares** *[20:53]*: Pozval. 
**Jan Hůla** *[20:54]*: Ještě ti můžu říct, když jsem dělal tu reimplementaci těch paperů, tak už vlastně dva papery se podařili přesně reimplementovat. Fakt. 
**Jakub Bares** *[21:09]*: Jo? Wow. 
**Jan Hůla** *[21:10]*: No, no. Děláme to tak, že děláme separátně benchmark a separátně děláme ten model. Já mu nejdříve dám nějaký prompt, který vytvoří specifikaci toho benchmarku, pak se na to pustí Cloud Code, který naimplementuje ten benchmark, a pak to stejné se dělá pro ten model. Takže já mu řeknu, chci experiment v tabu luce číslo 1, první řádek, třetí sloupec. Jo, a on si z toho zjistí, které nemohlo teda musí reimplementovat, na kterém benchmarku ho musí otestovat a udělá mi zase nejdříve tu specifikaci a pak to začne kodovat. Jo. 
**Jakub Bares** *[21:52]*: Jo. A. 
**Jan Hůla** *[21:53]*: Jakože není to úplně plně manuální, že jsem tam musel, zkrátka to nechtělo fungovat, takže já jsem zjistil, že on si tam neuvědomil jednu věc, kterou jsem mu tam musel zase specifikovat. Ale jako je to brutál, je to celka jako Práce, která by mě trvala normálně jako týden, tak je za půl hodinky hotová. No. 
**Jakub Bares** *[22:13]*: Jasně, to je pecko. To je dobrý, to je dobrý. No. 
**Jan Hůla** *[22:17]*: Takže postupně budeme implementovat i další šlanky. My jsme si stáhli nějakých dalších šlanků na to témat, na ty grafové sítě, na tu blohskou splnitelnost. A postupně to zkrátka Replikujeme všechno a pak se o tom může napsat nějaký paper, nebo víme, jak to uchopit, protože ono se velmi píše paper o něčem, co je napůl automatické. Nebo napůl normální, protože jakmile tam vstupuje ten člověk, tak to je strašně těžko porovnatelné. Ty můžeš říct, že jsi měl zhruba dobrého člověka, který to l dobře a těžko se to porovnává, když není to úplně automatické. Ale určitě to vypadá slibně. Tak. 
**Jakub Bares** *[23:14]*: To je dobrý. Já. 
**Jan Hůla** *[23:17]*: Jsem si říkal, že já jsem udal takovou tu... Tady je ta query, která umožní vytáhnout všechny ty contributions. Tak potom můžeš to projet nějakým dalším pázík, která to naklastruje. Že ti řekne, tak tady jsou typy contributionů, co se týkají architektury, tady jsou typy contributionů, které se týkají učícího algoritmu, tady jsou typy contributionů, které se týkají dát. A pak vlastně by ti to udělalo knihovnu, kde by vlastně každý ten typ toho contributionů byl nějaký modul. Tam knihovna by se jmenovala, já nevím, GNN for SAT a teďka by tam byla .architectures, data, tečka, dělá, že vlastně vidíte automaticky, jakou udal knihovnu z těch z těch z těch paperů. Jo. 
**Jakub Bares** *[24:08]*: Jo, jo. Takže. 
**Jan Hůla** *[24:12]*: Knihovnu, která by mohla vlastně sloužit jako potom základ pro tu evoluci, že bys mohl vlastně kombinovat ty myšlenky a dělat nějakou nějaký nějakou z těch těch toho kodu. Jo. 
**Jakub Bares** *[24:28]*: Jo. A tady to na to, co děláme tady spolu, co na to navazuje, jak? No. 
**Jan Hůla** *[24:34]*: To je právě, že ty chceš jako ideálně mít tam tu fázi, že ty si stáhneš ty papery a teďka potřebuješ jako nějak zjistit, co v těch paperech je. Jo. Jo, potřebuješ zhradka nějak komunikovat s těmi papery, udělat si nějakou představu, protože já si jako myslím, že v praxi to zhradka nebude plně automaticky, že to se stáhne a že se to samo udělá, že ty musíš nějak do toho vstupovat. A tohle dynamické UI, to je vlastně ten interfejs, skrze který ty budeš komunikovat s těmi papery a zjišťovat, co vlastně je třeba doplnit. Protože. 
**Jakub Bares** *[25:09]*: Teďka dokážeš replikovat papery, ale nevíš který chceš replikovat a proč chceš replikovat. Já. 
**Jan Hůla** *[25:19]*: Se tak představuju, že většinu asi budeš jít replikovat. Ale nebudeš tím replikovat všechno, protože v těch paperech je plné experimentů, které dějako nezajímají. Tak budeš tím replikovat tu čistou baseline a budeš tím týkat benchmarky. OK. 
**Jakub Bares** *[25:34]*: Ale to se tady v AI poznamenej se, že vlastně tady je důležitý to, potřeba se zamyslet nad tím, co všechno má nebo nemá smysl replikovat. To možná by mohl být dobrý prompt, že to bude mít nějakou schopnost posoudit a rozlišit, co zapadá do toho kontextu a co nezapadá. Jako nějak to říct s ohledem na ty všechny papery a prostě nějak to jako zvážit, protože jasně, to je určitě důležité. Takže potom by tam mohlo být právě jako, že když zadáš ten task, který chceš udělat, tak ti to jako řekne prostě měl bys zreplikovat tohle, tohle a tohle třeba už zase ne, protože protože už to je zbytečný třeba, no, že by ti to mohlo jako poradit vlastně. No. 
**Jan Hůla** *[26:33]*: Jo. Možná že jo, no. Jakože tam je to takové trošku ošemetné, že někdy si jako neseš nechat radit. Někdy spíš chceš jako se dotazovat. Jasně. 
**Jakub Bares** *[26:44]*: Že. 
**Jan Hůla** *[26:45]*: Ti to pak jako otravuje, že ti to jako dává nějaké informace, které zvláď tě nezajímají. No. 
**Jakub Bares** *[26:49]*: Tohle je spíš, že ti to jako něco vyfiltruje, že to nějak dá priorytu něčemu jako jinýmu. Když tam nahráš 20 papirů, tak ono to bude těžké to narovat všechno na jednu skrýnu, že jo. Takže si myslím, že by to mělo být jako právě nějak chytrý, aby to jako dokázalo zvážet Vypadá to jako, že ještě. 
**Jan Hůla** *[27:22]*: Máte nějaké věci, které můžete vytvořit, Jakmile to které nahraješ celé do toho kontextu, tak on dělá ten attention, můžete že jo, ten Transformer musí dát vytvořit. Attention. 
**Jakub Bares** *[27:32]*: To by se dělalo, ty extrakce by se dělaly právě zvlášť. No. Pomocí těch extractorů, ale pak to extrahovaný by se hodil do HTML, víš? No. 
**Jan Hůla** *[27:45]*: Však jasně, no to jo. Jakmile to máš extrahované, tak právě dohromady celé. Já. 
**Jakub Bares** *[27:50]*: Si myslím, že bylo fajn tam mít ještě jeden view, kromě toho finálního HTML. Kde by to bylo jako tabulkové, kde by si měl takovej velkej dashboard nebo nějakou velkou tabulku, kde by si měl třeba možná, jak to říct, horizontálně ty papery třeba a k každému z nich nějaký důležitý atribute, jako řádky. A mohl byste takhle jako scrollovat nahoru a dolů, doprava, dolava a vlastně projíždět, jakoby projíždět, co všechno bylo extrahováno z těch pejprů. No. Já. 
**Jan Hůla** *[28:34]*: To zkusím najít. 
**Jakub Bares** *[28:49]*: Ty. 
**Jan Hůla** *[28:49]*: Používáš ten Fireflies? Jo. 
**Jakub Bares** *[28:53]*: Kolik. 
**Jan Hůla** *[28:53]*: To stojí? 9. 
**Jakub Bares** *[28:55]*: Dolarů asi. A. 
**Jan Hůla** *[28:57]*: Teda ono to jakože zaznamenává všechno co říkáme, pak to udělá nějakou summary, jo? No. 
**Jakub Bares** *[29:02]*: Já tu summary nepoužívám, já vždycky vztahnu ten skript, hodím to do kurzoru a normálně mu řeknu prostě hele o čem jsme se bavili, udělej mi jako co mám udělat za featury a prostě jakoby vygeneruju si v kurzoru cokoliv potřebu, ať už to jsou Plán práce, featury nebo cokoliv. Jo. Ale. 
**Jan Hůla** *[29:24]*: Teď jsem slyšel, že ještě mu mluvíš k těmu. Že mu říkáš, zapíš si... To. 
**Jakub Bares** *[29:29]*: Nevím, jestli funguje. To jsem si chtěl označit nějaký bod v tom transcriptu, aby se to potom všiml kudy se rozpíš. Jo. 
**Jan Hůla** *[29:39]*: Jo, jo. Tak počkej, já to zkusím najít. On. 
**Jakub Bares** *[29:45]*: Tady nebyl zkoušený, jestli to nějak výrazně pomáhá. Jo. Jde. 
**Jan Hůla** *[29:53]*: To vidět? Jo. Teď tady mám ty Contributions a vlastně mám tady jakoby různé způsoby, jak si je můžu vizualizovat. Tak tady dám třeba ten... Tato to dám. Jo, tady mám vlastně vždycky, ono mi to potom jako zklastrovalo, že vlastně typy contributionu zklastrovalo na nějaké témata, takže tady jeden typ contributionu, loss function and training design, a tady jsou jako všechny papery, které to, které mají tenhle ten typ contributionu. Jo. 
**Jakub Bares** *[30:31]*: Jo, jo. Jo. 
**Jan Hůla** *[30:32]*: To je takovýhle view, pak tady mám třeba... 
**Jakub Bares** *[30:38]*: Pak. 
**Jan Hůla** *[30:38]*: Tady mám tenhle ten view, kde vlastně zase mám ten tip toho contributionu a pak tady mám ty papers. A když si to, tak tady to nejde rozkliknout. No tady mám tady několik views, mám tady třeba takovouhle tabulku, kde tady nahoře jsou ty tipy a tady mám každý ten paper a vidím, co v tom paperu jsou za tipy těch contributionů. A pak mám ještě jeden tady skript, nebo stránku, kde mám tady experimenty v daném článku. Takže si můžu rozkliknout ten článek. Teďka vidím, co jsou tam hlavní experimenty. Tady jsou vedlejší experimenty, nějaké emulation studies a tak. A když si kliknu na ten experiment, tak tady potom vidím, jaký tam byl benchmark, jaké tam byly baseliny. 
**Jakub Bares** *[31:37]*: A. 
**Jan Hůla** *[31:38]*: Tak dále. Takže to je to, co jsem říkal. Já jsem mu řekl, jaké informace chci, a on mi zkrátka na míru ušil tohleto UI. Jo. 
**Jakub Bares** *[31:46]*: Jo, jo. No. Přišel tady to HTML, jo? To. 
**Jan Hůla** *[31:58]*: Je HTML, takže jistě, to je vlastně tahleto stránka, je tam nějaký JavaScript, jsou embednuty, nebo ten je tady vlastně vokem. 
**Jakub Bares** *[32:08]*: Tak když někdo pošle, prosím mě tady toho, tyhle tomu. Jo. To je v pohodě. Dobré. Tak. 
**Jan Hůla** *[32:22]*: Jo, já ti to pošlu za chvilku a pak se můžeme spojit někdy. Já teďka budu mít to přes ty deny celkem nabité. Můžeme. 
**Jakub Bares** *[32:29]*: To v pátek. V. 
**Jan Hůla** *[32:30]*: Pátek možná mohli, že? No. 
**Jakub Bares** *[32:32]*: No, no. Tak. 
**Jan Hůla** *[32:33]*: Já ti ještě napišu přesně v koli a dáš mi vědět, jestli máš prostor. Jo. A domluvíme se za běhu. Dobře. 
**Jakub Bares** *[32:41]*: Tak jo. Super. 
**Jan Hůla** *[32:43]*: Tak jo, tak zatím. Tak. 
**Jakub Bares** *[32:45]*: Zatím, měj se, ahoj. 
