# TODO.md

Cose da fare:

### To Do
- [ ] Quale strategia scegliere per mostrare le possibili traduzioni nella pagine commnunity.html
    - `SELECT * ` non è scalabile, andrà tolto
    - implementare delle API sono la scelta migliore
        - Visualizzare prime dieci bad translations
        - Ordinare badTranslations in base alla colonna complaints
        - api che carica 10 entries del db
        - stesso approccio per possibleBetterTranslations
        - ATTENZIONE perché bisogna ordinare tutte le badTranslations prima di presentare le prime 10 dato che la select non mantiene l'ordine
- [ ] Usare i cookie per non far commentare troppo gli utenti
- [ ] Provare a trainare modello italiano/inglese o inglese/italiano (documentazione https://github.com/argosopentech/argos-train) (+docker)

### In Progress
- [ ] Stringhe vuote nel DB, mostrare questo errore sul front-end
    -   il back-end non inserisce stringhe vuote nel DB

### To be approved
- [ ] Pagina about.html
- [ ] Modifiche index.html e community.html
