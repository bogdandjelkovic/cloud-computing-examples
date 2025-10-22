# I Codebase

**Ispunjeno**

**Objašnjenje:** Aplikacija koristi jedan zajednički codebase koji se verzioniše u TFS-u. Sav razvoj se odvija na trunk grani, dok se iz nje kreiraju grane koje se koriste za različita okruženja — INT, UAT, i PROD. Merge-ovi se rade isključivo uz code review, što održava kvalitet i konzistentnost koda kroz sva okruženja.

**Druge opcije za poboljsanje:** Razmatran je prelazak na GIT, ali bi se pri prelasku izgubila istorija promena a i takodje sistemi su previse prilagodjeni radu preko TFS, pa bi tu došlo do prevelikih promena. Veliko planiranje bi bilo potrebno

# II Dependencies

**Ispunjeno**

**Objašnjenje:** Backend je razvijen u .NET Core-u, gde svaki projekat unutar solution-a ima svoj SDK .csproj fajl u kojem su sve zavisnosti jasno definisane i verzionisane putem nuget paket menadzera. UI je kreiran u Angular-u, gde su sve zavisnosti navedene u package.json fajlu i instaliraju se putem npm-a. Korisceni u lock fajlovi na UI projektu.

# III Config

**Ispunjeno**

**Objašnjenje:**
Konfiguracija aplikacije je centralizovana. Primarne vrednosti se čuvaju u Azure App Configuration servisu. Osetljive vrednosti se preuzimaju iz Azure Key Vaulta. Dodatne konfiguracije se prenose putem environment varijabli. Za lokalni development se koristi `appsettings.Development.json` fajl.

# IV Backing Services

**Delimicno ispunjeno**

**Objašnjenje:** Aplikacija koristi Dependency Injection (DI) i Inversion of Control (IoC), pri čemu se sve zavisnosti registruju tokom startup procesa na osnovu konfiguracije.

Međutim, dodavanje nove integracije zahteva inicijalnu implementaciju u kodu, nakon čega se promene u radu mogu vršiti samo kroz konfiguraciju — bez potrebe za novim buildom.

# V Build, Release, Run

**Delimično ispunjeno, u tranziciji ka punom ispunjenju**

**Objašnjenje:** Trenutno se build pokrece ručno putem CCTray alata, koji zatim automatski radi deploy aplikaciju na INT okruženje.
Međutim, u toku je prelazak na potpuno automatizovani CI/CD proces putem Azure DevOps pipeline-a, gde ce se:

1. build pokretati automatski na svaki commit u trunk ili drugi definisani branch
2. izvršavati linting, SonarQube analiza i code quality check
3. build biti oboren ako neki od provera ne uspe

Release faza kontrolisati kroz definisane stage-ove i environment approval-e.

Ovo će omogućiti jasnu separaciju između build, release i run faza, u potpunosti usklađenu sa 12-factor principom.

# VI Processes

**Ispunjeno**

**Objašnjenje:** Aplikacija se sastoji od više stateless procesa, uključujući background servise implementirane putem `IHostedService`` interfejsa, koji podržavaju graceful shutdown mehanizam.

Svi podaci o stanju aplikacije i korisnicima čuvaju se u bazi podataka, uz aktivno logovanje svih promena.

Za privremene podatke i cesto pristupane vrednosti koristi se in-memory cache, dok se u multi-server okruženju sinhronizacija između instanci obavlja preko Azure Service Bus-a, čime se obezbeđuje konzistentnost podataka i nezavisnost procesa.

# VII Port Bindingd

**Delimično ispunjeno, u tranziciji ka potpunom ispunjenju**

**Objašnjenje:**

- **Single server:** Aplikacija je hostovana na IIS-u u okviru jednog VM-a. Glavna Web App i pomoćni Web API servisi su dostupni kao podrute glavne aplikacije. Background servisi se pokreću kao Windows servisi na istom VM-u.

- **Multi-server:** Na svakom serveru se pokreću svi navedeni servisi, a synchronizacija između instanci vrši se preko Azure Service Bus-a.

- **Migracija u toku:** Prelazak na Azure WebApp sa auto horizontal scaling-om za web servise i WebJobs za background servise, što će omogućiti da svaki servis direktno izlaže portove kroz WebApp infrastrukturu i potpuno ispunjava 12-factor princip.

# VIII Concurrency

**Delimično ispunjeno**

**Objašnjenje:** Za web servise aplikacija se može skalirati horizontalno kroz više instanci (multi-server setup), što omogućava obradu većeg broja zahteva. Radimo na migraciji ka App Service Azure resursu koji bi olaksao horizontalno skaliranje.

Background servisi se hostuju samo na jednoj instanci/VM-u, čime se izbegava dupliciranje posla i konflikti. Radi se na prelasku na Web Jobs/Azure Functions.

Sticky session se ne koristi, vec je za sve web zahteve stateless.

# IX Disposability

**Objašnjenje:** Aplikacija podržava graceful shutdown, što znači da se svi background servisi i otvorene konekcije pravilno zatvaraju prilikom zaustavljanja procesa.

# X Dev/prod parity

**Ispunjeno**

**Objašnjenje:** Ddev, INT, UAT i produkcijsko (PROD) okruženje koriste razlicite resurse, sto znaci da baze, Azure resursi i drugi servisi nisu identični između okruženja.

Takođe, svaki klijent ima svoje odvojene resurse.

# XI Logs

**Ispunjeno**

**Objašnjenje:** Aplikacija koristi Serilog i  Application Insights za logovanje.

Postoji exception handling middleware koji hvata greške i loguje ih, pritom externe servise obavestava genericki da je doslo do greske ali ne oktriva sta je problem.

Logovi se tretiraju kao event stream, što omogućava praćenje, agregaciju i analizu bez potrebe za direktnim pristupom samoj aplikaciji.

# XII Admin processes

**Ispunjeno**

**Objašnjenje:** Administrativni i management taskovi (npr. migracije baze, batch jobovi, čišćenje podataka) se pokreću kao zasebni, one-off procesi.

Oni se aktiviraju prilikom pipeline deploy-a ili po potrebi, a ne kao deo glavne aplikacije, što omogućava jasnu separaciju funkcionalnosti i poštovanje 12-factor principa.