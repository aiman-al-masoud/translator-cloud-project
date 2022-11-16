# TODO.md

Cose da fare:

### To Do
- [ ] Fare pagina about.html
- [ ] Quale strategia scegliere per mostrare le possibili traduzioni nella pagine commnunity.html
    - `SELECT * ` non è scalabile, andrà tolto
    - forse delle API sono la scelta migliore
    
    - Visualizzare prime dieci bad translations
    - Ordinare badTranslations in base alla colonna complaints
    - api che carica 10 entries del db
    - stesso approccio per possibleBetterTranslations
    
- [ ] Provare a trainare modello italiano/inglese o inglese/italiano (documentazione https://github.com/argosopentech/argos-train) (+docker)

### In Progress
- [ ] Stringhe vuote nel DB, mostrare questo errore sul front-end
    -   il back-end non inserisce stringhe vuote nel DB

### Done ✓
