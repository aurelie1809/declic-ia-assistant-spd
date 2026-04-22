# Déclic IA — Assistant SPD

Application web de génération de Scénarios Pédagogiques Détaillés sur mesure.  
Développée par Aurélie MAUNIE — Déclic IA / LudomaIA.

---

## Déploiement en 5 étapes

### Étape 1 — Créer le dépôt GitHub

1. Va sur [github.com](https://github.com) et connecte-toi.
2. Clique sur **"New repository"** (bouton vert en haut à droite).
3. Nomme-le : `declic-ia-assistant-spd`
4. Laisse-le **Public** (nécessaire pour le plan gratuit Render).
5. Ne coche rien d'autre. Clique **"Create repository"**.

### Étape 2 — Déposer les fichiers

Dans la page du dépôt vide, clique **"uploading an existing file"**.  
Glisse-dépose ces 3 fichiers :
- `server.py`
- `index.html`
- `render.yaml`

Clique **"Commit changes"**.

### Étape 3 — Créer le service sur Render

1. Va sur [render.com](https://render.com) et connecte-toi.
2. Clique **"New +"** puis **"Web Service"**.
3. Connecte ton dépôt GitHub `declic-ia-assistant-spd`.
4. Render détecte `render.yaml` automatiquement.
5. Clique **"Create Web Service"**.

### Étape 4 — Ajouter ta clé API (IMPORTANT)

Dans le dashboard Render, sur ton service :
1. Va dans **"Environment"** (menu de gauche).
2. Clique **"Add Environment Variable"**.
3. **Key :** `ANTHROPIC_API_KEY`
4. **Value :** ta clé Anthropic (commence par `sk-ant-...`).
5. Clique **"Save Changes"**. Render redémarre le service.

Ta clé est stockée de façon sécurisée. Elle n'apparaît jamais dans le HTML.

### Étape 5 — Récupérer ton URL publique

Render te donne une URL du type :  
`https://declic-ia-assistant-spd.onrender.com`

C'est l'URL de ton application publique.  
Tu peux l'intégrer dans Google Sites via **Insertion > Intégrer une URL**.

---

## Fonctionnement local (test sur ton ordinateur)

1. Définis ta clé dans le terminal :
   - Mac/Linux : `export ANTHROPIC_API_KEY=sk-ant-...`
   - Windows : `set ANTHROPIC_API_KEY=sk-ant-...`
2. Lance le serveur : `python server.py`
3. Ouvre : `http://localhost:8080`

---

## Notes importantes

- **Plan gratuit Render :** le service se met en veille après 15 min sans activité. Le premier appel après une pause prend 30 à 60 secondes. Acceptable pour un usage Déclic IA.
- **Non certifié Qualiopi :** le SPD généré ne mentionne ni Qualiopi, ni CPF, ni OPCO.
- **TVA :** mention légale automatique dans chaque SPD généré (art. 293 B du CGI).

---

Aurélie MAUNIE — ludomaia41400@gmail.com
