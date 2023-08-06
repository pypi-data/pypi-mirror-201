# Coding Pirates Kuglebane controller

Controlleres er lavet til [Coding Pirates Viborg/Bjerringbro](http:kodepirat.dk)s kuglebane-projekt i forårssæsonen 2023.

Controlleren kan modtage et (simpelt) serielt signal med en kommando - f.eks. fra en fra micro:bit.

Ud fra den modtagne kommando sender controlleren et request til [_kuglebane centralen_](https://github.com/Coding-Pirates-Viborg/kuglebane-central) og sender efterfølgende et svar tilbage til micro:bit'en.

Når controlleren starter op (se afsnit herunder) startes en tråd der poller _kuglebane centralen_ for at høre om der er kommet events til den kuglebane controlleren er tilknyttet.

- [Coding Pirates Kuglebane controller](#coding-pirates-kuglebane-controller)
  - [Installation af kuglebane-controlleren](#installation-af-kuglebane-controlleren)
  - [Start kuglebane controlleren](#start-kuglebane-controlleren)
    - [Konfiguration af micro:bit og kuglebane-central](#konfiguration-af-microbit-og-kuglebane-central)
    - [Forbinde micro:bit til controlleren](#forbinde-microbit-til-controlleren)
    - [Login med API bruger ved opstart](#login-med-api-bruger-ved-opstart)
    - [Controller initialiseres ved opstart](#controller-initialiseres-ved-opstart)
    - [Hentning af beskeder til kuglebanen i baggrunden](#hentning-af-beskeder-til-kuglebanen-i-baggrunden)
    - [Logning af kommunikation i konsollen](#logning-af-kommunikation-i-konsollen)
  - [Kommandoer der kan sendes til controlleren](#kommandoer-der-kan-sendes-til-controlleren)
    - [Kommando: `init:<<bane_id>>`](#kommando-initbane_id)
    - [Kommando: `send:<<til_bane_id>>`](#kommando-sendtil_bane_id)
    - [Kommando: `events`](#kommando-events)
    - [Kommando: `pop`](#kommando-pop)
    - [Kommando: `pop:<<event_id>>`](#kommando-popevent_id)
    - [ERROR: ukent kommando](#error-ukent-kommando)
  - [Micro:bit emulator](#microbit-emulator)
  - [Eksempelkode til micro:bit'en](#eksempelkode-til-microbiten)
  - [Finde den port micro:bit'en kommunikerer på](#finde-den-port-microbiten-kommunikerer-på)
    - [Linux (Pi)](#linux-pi)
      - [Installere screen på Ubuntu](#installere-screen-på-ubuntu)
    - [Mac](#mac)

## Installation af kuglebane-controlleren

Det anbefales at installere controlleren i et virtuelt miljø.

1. Lav en mappe, hvor du vil have controlleren installeret
1. Start en kommandoprompt/Terminal og gå ind mappen 
1. Lav et virtuelt environment inde i mappen ved at skrive: \
    ```text
    python -m venv venv
    ```
   - _der kan godt gå lidt tid, før det er oprettet_
1. Aktiver “venv” med: 
   ```
   activate
   ```
   \
  eller (Windows): \
    ```
    venv\Scripts\activate
    ```
1. Du kan se at det virtuelle miljø er aktiveret, når det står (venv) forrest i kammondo-prompten - f.eks.:\
    ```
    (venv) kuglebane-controller $
    ```
1. Installer kuglebane controlleren med pip

      ```text
      pip intall kb-controller
      ```

Husk at installere Python først :-)

## Start kuglebane controlleren

Denne kan startes fra et aktiveret `venv`:

```
  python venv/lib/python3.7/site-packages/kb_controller/controller.py
```
 
- **Bemærk**: _i Windows, ser det typisk sådan ud:_

```
  python venv\Lib\site-packages\kb_controller\controller.py
```


eller via Python med `kb_controller.controller.start()` 

F.eks.:

```python
>>> from kb_controller import controller
>>> controller.start()
```


eller fra source filen (hvis koden er klonet fra Github):

```text
  python src/kb_controller/controller.py
```


### Konfiguration af micro:bit og kuglebane-central
Første gang controlleren startes oprettes en `kbc-config.ini` konfigurationsfil, hvor port-angivelse til micro:bit'en, url'en til kuglebanecentralen og polling-intervallet til kuglebanecentralen angives. 

Der kan være forskllige konfigurationer, afhængigt af om micro:bit'en emuleres og om man bruger en lokal version af kuglebane-centralen eller ej. Dette styres med disse to flag i konfig-filen:

```
is_production = True eller False
is_emulator = True eller False
```

Som standard er controlleren sat op til at bruge _kuglebane centralen_ der ligger "i skyen" (på  https://kuglebane.pythonanywhere.com) og er sat til at spørge hvert minut (`polling_interval=60`) om der er beskeder til den kuglebane, controlleren hører til.

Tilret konfigurationsfilen, så den passer med hvilken seriel port micro:bit'en er forbundet til (se næste afnsit).

### Forbinde micro:bit til controlleren
Controlleren forventer at der sidder en enhed på den serielle port - f.eks. en micro:bit (_eller emulatoren - se herunder_).

Hvis der ikke kan skabes forbindelse på angivne serielle port stopper controlleren med en fejl og lister de porte der lige nu er tilgængelige. 

Hvis du tilslutter micro:bit'en (via USB kablet), så hold øje med den port der hedder noget med "USB" og/eller "microbit", f.eks.:

```text
  -------------------------------------
  FEJL under etablering af forbindelse!
  (2, "could not open port /dev/cu.usbmodem1410: [Errno 2] No such file or directory:")

  Tjek om microbit'en er forbundet, eller om portnavnet er korrekt.

  Tilgængelige porte:
  /dev/cu.BLTH - n/a
  /dev/cu.Bluetooth-Incoming-Port - n/a
  /dev/cu.usbmodem14102 - BBC micro:bit CMSIS-DAP - mbed Serial Port      <--
  -------------------------------------
```
for Windows, vil det være en af `COM` portene (f.eks. `COM4`)

Åbn filen _kbc-config.ini_ og ret værdien for porten i `[MICROBIT]` afsnittet, f.eks:

```text
  [MICROBIT]
  tty_name = COM4
```


### Login med API bruger ved opstart
Når den serielle port er forbundet, skal api-bruger og adgangskode angives. API brugeren, er den bruger der har adgang til at lave forespørgsler til _kuglebane centralen_ (se evt. også https://kuglebane.pythonanywhere.com)


### Controller initialiseres ved opstart

Når controlleren er startet op skriver den ud i konsollen hvilken afdeling den hører til og hvilke kommandoer man kan sende til den.

Herefter venter den på at der sende en `init` kommando fra microbit'en, der fortæller hvilken kuglebane den tilhører. Dette gøres ved at få micro:bit'en til at sende en `init:<<ID>>` kommando, hvor `ID` er kuglebanens ID (en oversigt over kuglebane-ID'er kan ses på _kuglebane centralen_ - https://kuglebane.pythonanywhere.com/tracks/)

Se desuden afsnittet _Kommandoer der kan sendes til controlleren_ herunder.

Når controlleren har fået at vide hilken kuglebane den tilhører skrives listen af kuglebaner per afdeling ud i konsollen, f.eks.:

```text
  ============================================================
    M I C R O : B I T   S E R I A L   C O N T R O L L E R
  ============================================================
  Kuglebane central........: https://kuglebane.pythonanywhere.com/
  API bruger...............: CpvApi
  Controller for afdeling..: CPV
  -----------------------------------------------------------

  [2023-03-19 22:56:16] m:b <<< init:1

  -----------------------------------------------------------
  Tilgængelige kuglebaner:

    CPV (egen afdeling):
    -------------------------------------
      1 - Gargamel
      2 - Smølfine    [CONTROLLER]
    -------------------------------------

    CPB:
      3 - Gammelsmølf
      4 - Stærkesmølf

    CPS:
      5 - Astrosmølf
  -----------------------------------------------------------

  [2023-03-19 22:56:16] m:b >>> OK:INIT:1
```

Controlleren herover er placeret i afdeling _CPV_ og tilsluttet kuglebane _Smølfine_ med ID = 2.

### Hentning af beskeder til kuglebanen i baggrunden

Når controlleren er startet op og initialiseret, startes en tråd, der står og poller _kuglebane centralen_ om der er kommet events til den kuglebane, controllere er tilsluttet. 

Dette gøres i det interval (i sekunder) der er sat i `polling_interval` i _kbc-config.ini_ filen (se tidligere afsnit).

Hvis der er en eller flere events, skrives dette ud i konsollen, f.eks.:

```text
  - - - - - - - - - - - - - - - - - - - - -
  Henter events fra kukglebane centralen...

  [2023-03-19 23:09:18] KB-CENTRAL >>> https://kuglebane.pythonanywhere.com/api/events/1  [GET]
  [2023-03-19 23:09:18] KB-CENTRAL <<< Response status OK!


  Event id: 1 - kommando: START
    - afsendt: 19-03-2023 23:08:41.787930
    - fra CPB, bane 3 (Gammelsmølf)


  Antal events modtaget i alt: 1

  Kontakter kuglebane-centralen igen om 60 sekunder...
  - - - - - - - - - - - - - - - - - - - - -
```


Det er så op til micro:bit'en at hente en event.

Nu og her, gøres dette ved at bruge `pop` kommandoen - så man henter den ælste event, der er sendt, hvorefter denne slettes fra _kuglebane centralen_.

### Logning af kommunikation i konsollen

Generelt skrives al kommunikation ud i konsollen. Ud over tidsstemplet, benyttes der disse præfiks:

- `m:b >>>` besked sendt TIL micro:bit
- `m:b <<<` besked modtaget FRA micro:bit
- `KB-CENTRAL >>>` request send TIL _kuglebane centralen_
- `KB-CENTRAL <<<` response modtaget FRA _kuglebane centralen_

Så hvis der opstår kommunikationsfejl et eller andetr sted, kan man forsøge at spore det ved at kigge i konsollen.

---

## Kommandoer der kan sendes til controlleren

Hver gang en kommando modtages vil controlleren svare på formen:  `STATUS:KOMMANDO:SVAR`

Hvor: 

* STATUS = `OK` eller `ERROR`
* KOMMANDO = den kommando der er modtaget
* SVAR = for `OK` er dette svaret på kommandoen og for `ERROR` er dette noget yderligere fejlinformation

Svarene er uddybet herunder.

P.t. understøttes disse kommandoer:

---
### Kommando: `init:<<bane_id>>`

Initialisere controlleren til den kuglebane (med id=`bane_id`), som controlleren er tilknyttet.

* **Svar fra controller**: `OK:INIT:<<bane_id>>`

* **Svar hvis der opstår en fejl:**: `ERROR:INIT:<<bane_id>>:<<eventuel fejlbesked>>`

---
### Kommando: `send:<<til_bane_id>>`

Sender en `START` event til bane `<<til_bane_id>>`

* **Svar fra controller**: `OK:SEND:<<fra-bane_id>>:<<til-bane_id>>`

Hvor `fra-bane_id` er ID på den kuglebane, som controllren selv er tilsluttet.

* **Svar hvis der opstår en fejl:**: `ERROR:SEND:<<til_bane_id>>:<<eventuel fejlbesked>>`

---
### Kommando: `events`

Henter alle events der er sendt til den kuglebane controlleren er tilsluttet (dvs. kuglebanen man har angivet fra micro:bit'en med `init` kommandoen)

* **Svar fra controller**: `OK:EVENTS-TRACK:<<bane_id>>:<<antal-events>>`
  * `bane_id` = den kuglebane controlleren er tilnkyttet (_dvs. det ID der er modtaget fra micro:bit'en med_ `init` _kommandoen_)
  * `antal_events` = antallet af beskeder der er modtaget til denne kuglebane

Beærk: i svaret ses bare antallet af events. Kig på konsollen for controlleren for at se hvilke events der er modtaget. 

For at afvikle den første (ældste) event sendes `pop` kommandoen.

For at afvikle en bestemt event sendes `pop:<<event_id>>` kommandoen

* **Svar hvis der opstår en fejl:**: `ERROR:EVENTS:<<eventuel fejlbesked>>`


---
### Kommando: `pop`

Fjerner den ældste event fra _kuglebane centralen_ og sender kommando-id fra eventen til enheden (f.eks. en micro:bit) på den serielle port, så denne kan udføre kommandoen (f.eks. `START` for at starte en kugle) på kuglebanen den er tilnkyttet.

Desuden medsendes hvilken afdeling og kuglebane eventen blev afsendt fra.

* **Svar fra controller**: `OK:POP:<<fra_afdeling>>:<<fra-bane_id>>:<<kommando_id>>` 

  * EKSEMPEL: ældste besked er et `START` event afsendt fra afdeling `CPB` kuglebane nr. `2`:  `OK:POP:CPB:2:START`

* **Svar hvis der opstår en fejl:**: `ERROR:POP:<<eventuel fejlbesked>>`


---
### Kommando: `pop:<<event_id>>`

_ENDNU IKKE IMPLEMENTERET!_

Samme som `pop` men med et specifikt `<<event_id>>` i stedet for den ældste event. 

* **Svar fra controller**: `OK:POP:event_id:kommando_id` - f.eks. `OK:POP:6:START`

---

### ERROR: ukent kommando
Hvis der modtages ne kommando, der ikke er en af ovenstående, sendes denne fejl:

* `ERROR:unknown-command`

Hvilket også vil være tilfældet, hvis den kommando der sendes fra micro:bit'en af en eller anden årsag bliver korrupt (f.eks. pga. støj på kablet el.l.).

Man kan derfor overveje at lade micro:bit'en forsøge igen et par gange, hvis den modtager et fejlsvar.

---


## Micro:bit emulator

P.T. IKKE UNDERSTØTTET I WINDOWS!

Med `ubit_emulator.start(<<track_id>>)` startes en simpel emulator, hvor man kan emulere de tekst kommandoer der sendes fra f.eks. en micro:bit der er forbundet serielt til controlleren.

Emulatoren defaulter til track-id=1. Dette skal sættes til det ID der passer med en kuglebane i den forening, controlleren er konfigureret til.

For at sætte emulatoren til at "lege" kugelbane 3, sættes `track_id=3` i start parameteren, f.eks:

```python
>>> from kb_controller import ubitemulator
>>> ubitemulator.start(3)
```

eller fra et aktiveret `venv`:

```
  python venv/lib/python3.7/site-packages/kb_controller/ubitemulator.py 3
```

eller (hvis koden er klonet fra Github):

```text
  python src/kb_controller/ubitemulator.py 3
```

Når emulatoren starter, skriver den hvilken seriel port den er startet på og hvilket track ID den er startet op med, f.eks.:

```text
=============================
     micro:bit emulator
=============================

Brug denne port på controlleren:
--------------------------------

/dev/ttys006

--------------------------------

micro:bit track-ID: 3

Venter på controller...

```

Og den venter nu på en `init` forespørgsel fra controlleren, som emulatoren svarer på. Herefter kan man sende en vilkårlig kommando til controlleren.

```
--------------------------------

micro:bit track-ID: 1

Venter på controller...
Controller forbundet.
Sender bane-ID "3" til controller
--> init:1

<-- OK:INIT:3
Emulator klar - skriv kommando og tryk <Enter>

Skriv kommando: 
```


## Eksempelkode til micro:bit'en

Et eksempel, hvor micro:bit'en kan modtage og sende kan ses i 

https://github.com/Coding-Pirates-Viborg/microbit-controller


## Finde den port micro:bit'en kommunikerer på

### Linux (Pi)

1. Plug in the micro:bit and open a new terminal window.
2. Typing dmesg | tail will shows you which /dev/ node the micro:bit was assigned (e.g. /dev/ttyACM0).
3. UBUNTU: dmesg | grep tty
4. Type sudo screen /dev/tty0 115200, replacing the number with the number you found in the previous step. You may need to install the screen program if you don't already have it.
5. To exit, press Ctrl-A then Ctrl-D.

Eks på tty for micro:bit’en: ttyACM0: USB ACM device

#### Installere screen på Ubuntu

- sudo apt install screen

### Mac

1. Plug in the micro:bit and open a new terminal window.
2. Type `ls /dev/cu.\*` to get a list of connected serial devices; one of them will look like /dev/cu.usbmodem1422 (the exact number depends on your computer).
3. Type `screen /dev/cu.usbmodem1422 115200`, replacing the 'usbmodem' number with the number you found in the previous step. This will open the micro:bit's serial output and show all messages received from the device.
4. To exit, press Ctrl-A then Ctrl-D.
