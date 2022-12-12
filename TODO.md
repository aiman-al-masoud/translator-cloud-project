# TODO.md

## Fourth Release
### To Do
- Implementare le **web socket** ed un micro-servizio dedicato ai voti/possibleBetterTranslations? Oppure fare refrash della pagina ogni N secondi?
- Usare i cookie-IP-[fingerprint](https://github.com/fingerprintjs/fingerprintjs) per non far commentare troppo gli utenti


## Future Updates
- Provare a trainare modello italiano/inglese o inglese/italiano (documentazione https://github.com/argosopentech/argos-train) (+docker)
- Login degli utenti alla community page

## More Future Updates
- **API gateway** o **ELB** per fare instradamento del traffico, sulla base del path (coppia delle lingue), al container dedicato

- **Training parallelizzabile**: usare più GPU per ridurre i tempi

- **Disaster Recovery**: Infrastructure as a Code
    - non solo cross-region
    - anche cross-account
    - tenere un backup dello stato (modelli + database)
    - *Terraform* -> mantiene la descrizione delle struttura

- **CI/CD**: automatizzare il deploy del codice sul cloud
    - testare il codice in automatico (anche con *SonarCube*)

## Maybe never
- **AB testing**

- **Ground truth**: verificare la bontà del nuovo modello

## Decisions
- Usiamo il DB **neo4j**
    - buona velocità nella ricerca muovendosi nel grafo
    - ottima velocità nella creazione di nuove relazioni
    - constraints a priori -> si può fare una semi-struttura (al posto di mongoDB)
    - distribuito ?
    - sharding non possibile