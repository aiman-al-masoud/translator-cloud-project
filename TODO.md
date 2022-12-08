# TODO.md

## Fourth Release
### To Do
- Studiare l'architettura
- Implementare le **web socket** ed un micro-servizio dedicato ai voti/possibleBetterTranslations? Oppure fare refrash della pagina ogni N secondi ? 


## Future Updates
- Usare i cookie-IP per non far commentare troppo gli utenti
- Provare a trainare modello italiano/inglese o inglese/italiano (documentazione https://github.com/argosopentech/argos-train) (+docker)

## More Future Updates
- **API gateway** o **ALB** per fare instradamento del traffico, sulla base del path (coppia delle lingue), al container dedicato
- Training parallelizzabile? Nel in senso di usare più GPU
- **Disaster Recovery**: Infrastructure as a Code
    - non solo cross-region
    - anche cross-account
    - tenere un backup dello stato (modelli)
    - Terraform -> mantiene la descrizione delle struttura
- **CI/CD**: automatizzare il deploy del codice sul server
    - testare il codice in automatico (anche con *SonarCube*)
- AB testing
- Groung truth: verificare la bontà del nuovo modello
