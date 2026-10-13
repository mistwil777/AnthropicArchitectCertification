# Module 1 — Conception de plateformes et de solutions Claude

## Les 4 décisions architecturales

Concevoir une solution Claude = répondre à 4 questions dans cet ordre. Chaque décision contraint la suivante.

:::mermaid
flowchart LR
  D1["1 - Decomposition"]
  D2["2 - Pattern"]
  D3["3 - Architecture"]
  D4["4 - Modele + Entree"]
  D1 --> D2 --> D3 --> D4
  style D1 fill:#1c1f2e,stroke:#4f8ef7,color:#ddd8f0
  style D2 fill:#1c1f2e,stroke:#a78bfa,color:#ddd8f0
  style D3 fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style D4 fill:#1c1f2e,stroke:#fbbf24,color:#ddd8f0
:::

**Exemple fil rouge :** assistant de traitement de sinistres d'assurance.
- D1 : Claude lit + rédige / SQL vérifie la couverture / Humain valide > 5 000 £
- D2 : Workflow (étapes connues à l'avance, coût d'erreur élevé)
- D3 : RAG sur les polices d'assurance
- D4 : claude-sonnet, context window compressée, API directe

:::rule
**Séquence obligatoire.** Sauter D1 pour aller à D4 = optimiser la latence d'un système mal décomposé.
:::

## Comment Claude se comporte

### Les 4 propriétés fondamentales

:::mindmap
<svg viewBox="0 0 880 185" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif" font-size="11">
  <rect x="5" y="5" width="208" height="175" rx="7" fill="#1c1f2e" stroke="#4f8ef7" stroke-width="1.5"/>
  <text x="109" y="27" fill="#4f8ef7" font-size="11" font-weight="bold" text-anchor="middle">TOKEN PREDICTION</text>
  <text x="109" y="43" fill="#7874a0" font-size="9" text-anchor="middle">Non-déterministe</text>
  <line x1="15" y1="51" x2="203" y2="51" stroke="#2e3250"/>
  <text x="15" y="67" fill="#2dd4a0" font-size="10">✓ Instructions concrètes</text>
  <text x="15" y="82" fill="#2dd4a0" font-size="10">✓ Formats définis</text>
  <text x="15" y="103" fill="#f87171" font-size="10">✗ Calculs exacts</text>
  <text x="15" y="118" fill="#f87171" font-size="10">✗ Instructions ambiguës</text>
  <text x="15" y="143" fill="#7874a0" font-size="9">→ eval + structured output</text>
  <text x="15" y="158" fill="#7874a0" font-size="9">→ reformuler l'objectif</text>
  <rect x="223" y="5" width="208" height="175" rx="7" fill="#1c1f2e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="327" y="27" fill="#a78bfa" font-size="11" font-weight="bold" text-anchor="middle">KNOWLEDGE</text>
  <text x="327" y="43" fill="#7874a0" font-size="9" text-anchor="middle">Figée à l'entraînement</text>
  <line x1="233" y1="51" x2="421" y2="51" stroke="#2e3250"/>
  <text x="233" y="67" fill="#2dd4a0" font-size="10">✓ Raisonnement général</text>
  <text x="233" y="82" fill="#2dd4a0" font-size="10">✓ Sujets courants</text>
  <text x="233" y="103" fill="#f87171" font-size="10">✗ Données privées</text>
  <text x="233" y="118" fill="#f87171" font-size="10">✗ Évolution rapide</text>
  <text x="233" y="143" fill="#7874a0" font-size="9">→ RAG · Tools · MCP</text>
  <text x="233" y="158" fill="#7874a0" font-size="9">→ source externe = référence</text>
  <rect x="441" y="5" width="208" height="175" rx="7" fill="#1c1f2e" stroke="#2dd4a0" stroke-width="1.5"/>
  <text x="545" y="27" fill="#2dd4a0" font-size="11" font-weight="bold" text-anchor="middle">CONTEXT WINDOW</text>
  <text x="545" y="43" fill="#7874a0" font-size="9" text-anchor="middle">Token budget fixe</text>
  <line x1="451" y1="51" x2="639" y2="51" stroke="#2e3250"/>
  <text x="451" y="67" fill="#2dd4a0" font-size="10">✓ Raisonnement sur corpus</text>
  <text x="451" y="82" fill="#2dd4a0" font-size="10">✓ Explicite et délimité</text>
  <text x="451" y="103" fill="#f87171" font-size="10">✗ Taille fixe</text>
  <text x="451" y="118" fill="#f87171" font-size="10">✗ Inclusion/ordre = coût</text>
  <text x="451" y="143" fill="#7874a0" font-size="9">→ prioriser · tronquer</text>
  <text x="451" y="158" fill="#7874a0" font-size="9">→ résumer · externaliser</text>
  <rect x="659" y="5" width="216" height="175" rx="7" fill="#1c1f2e" stroke="#fbbf24" stroke-width="1.5"/>
  <text x="767" y="27" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">STEERABILITY</text>
  <text x="767" y="43" fill="#7874a0" font-size="9" text-anchor="middle">Adapte au system prompt</text>
  <line x1="669" y1="51" x2="865" y2="51" stroke="#2e3250"/>
  <text x="669" y="67" fill="#2dd4a0" font-size="10">✓ Rôles · formats</text>
  <text x="669" y="82" fill="#2dd4a0" font-size="10">✓ Contraintes métier</text>
  <text x="669" y="103" fill="#f87171" font-size="10">✗ Dérive si contradictions</text>
  <text x="669" y="118" fill="#f87171" font-size="10">✗ Confiance ≠ validité</text>
  <text x="669" y="143" fill="#7874a0" font-size="9">→ system prompt clair</text>
  <text x="669" y="158" fill="#7874a0" font-size="9">→ tests de régression</text>
</svg>
:::

:::flashcards
Q: Token Prediction → conséquence architecturale principale ?
R: **Non-déterminisme** — même input, outputs différents. Nécessite des **evals**.

Q: Steerability : "confiance ≠ validité" — implication ?
R: Claude peut être très confiant et **faux simultanément**. La vérification est un choix architectural.

Q: Knowledge gap → atténuation ?
R: Système externe comme référence : **RAG, Tools, MCP**. Jamais la knowledge du modèle seul.

Q: Context window limit → consequence architecturale ?
R: Pas de memoire persistante native — il faut **externaliser** l'etat (base, fichier, memoire vectorielle).
:::

## Décomposition

:::mermaid
flowchart TD
  T[Tache] --> Q1{Donnees live en base ?}
  Q1 -- Oui --> SE[Systeme existant]
  Q1 -- Non --> Q2{Action irreversible ?}
  Q2 -- Oui --> H[Humain]
  Q2 -- Non --> Q3{Travail de langage ?}
  Q3 -- Oui --> C[Claude]
  Q3 -- Non --> SE2[Systeme existant]
  style SE fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style SE2 fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style H fill:#1c1f2e,stroke:#f87171,color:#ddd8f0
  style C fill:#1c1f2e,stroke:#4f8ef7,color:#ddd8f0
:::

:::rule
**Piège exam :** lookup de données existantes (garantie, stock, tier, politique publiée) → **Système existant**, même si ça ressemble à du jugement.
:::

:::situation
**Règle sinistre > £5 000 confiée à Claude :**
- 14 000 sinistres → 41 mal routés ("environ cinq mille livres" ≠ seuil déclencheur)
- Dérive silencieuse — détectée à l'audit, pas par le système
- Cause : règle déterministe confiée à un système probabiliste
:::

:::flashcards
Q: "Vérifier si la garantie s'applique à ce numéro de série" → qui ?
R: **Système existant** — lookup en base, pas un jugement.

Q: "Émettre le remboursement" → qui ?
R: **Humain** — action financière irréversible, même si l'éligibilité est automatique.

Q: Règle déterministe (ex : seuil £5 000) → erreur de décomposition ?
R: La confier à Claude. Les seuils exacts doivent aller au **Système existant** — Claude est probabiliste.

Q: Claude + outil externe = quel pattern minimum ?
R: **Augmented LLM** — un appel + tool/RAG. Pas encore un Workflow.
:::

## Les 7 primitives

:::mindmap
<svg viewBox="0 0 750 310" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif">
  <rect x="25" y="8" width="170" height="72" rx="7" fill="#1c1f2e" stroke="#4f8ef7" stroke-width="1.5"/>
  <text x="110" y="32" fill="#4f8ef7" font-size="12" font-weight="bold" text-anchor="middle">Tools</text>
  <text x="110" y="50" fill="#ddd8f0" font-size="10" text-anchor="middle">Agir</text>
  <text x="110" y="68" fill="#7874a0" font-size="9" text-anchor="middle">fonction appelable par le modèle</text>
  <rect x="205" y="8" width="170" height="72" rx="7" fill="#1c1f2e" stroke="#4f8ef7" stroke-width="1.5"/>
  <text x="290" y="32" fill="#4f8ef7" font-size="12" font-weight="bold" text-anchor="middle">MCP</text>
  <text x="290" y="50" fill="#ddd8f0" font-size="10" text-anchor="middle">Connecter</text>
  <text x="290" y="68" fill="#7874a0" font-size="9" text-anchor="middle">protocole exposant un set de Tools</text>
  <rect x="385" y="8" width="170" height="72" rx="7" fill="#1c1f2e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="470" y="32" fill="#a78bfa" font-size="12" font-weight="bold" text-anchor="middle">Subagents</text>
  <text x="470" y="50" fill="#ddd8f0" font-size="10" text-anchor="middle">Isoler / paralléliser</text>
  <text x="470" y="68" fill="#7874a0" font-size="9" text-anchor="middle">contexte séparé, tâche délimitée</text>
  <rect x="25" y="100" width="170" height="72" rx="7" fill="#1c1f2e" stroke="#f87171" stroke-width="1.5"/>
  <text x="110" y="124" fill="#f87171" font-size="12" font-weight="bold" text-anchor="middle">Hooks</text>
  <text x="110" y="142" fill="#ddd8f0" font-size="10" text-anchor="middle">Garantir</text>
  <text x="110" y="160" fill="#7874a0" font-size="9" text-anchor="middle">code déterministe sur événement</text>
  <rect x="205" y="100" width="170" height="72" rx="7" fill="#1c1f2e" stroke="#fbbf24" stroke-width="1.5"/>
  <text x="290" y="124" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">Skills</text>
  <text x="290" y="142" fill="#ddd8f0" font-size="10" text-anchor="middle">Packager</text>
  <text x="290" y="160" fill="#7874a0" font-size="9" text-anchor="middle">procédure versionnée réutilisable</text>
  <rect x="25" y="195" width="255" height="72" rx="7" fill="#1c1f2e" stroke="#2dd4a0" stroke-width="1.5"/>
  <text x="152" y="220" fill="#2dd4a0" font-size="12" font-weight="bold" text-anchor="middle">Agent Teams</text>
  <text x="152" y="238" fill="#ddd8f0" font-size="10" text-anchor="middle">Coordonner des pairs</text>
  <text x="152" y="256" fill="#7874a0" font-size="9" text-anchor="middle">agents pairs — objectif partagé</text>
  <rect x="290" y="195" width="265" height="72" rx="7" fill="#1c1f2e" stroke="#2dd4a0" stroke-width="1.5"/>
  <text x="422" y="220" fill="#2dd4a0" font-size="12" font-weight="bold" text-anchor="middle">Dynamic Workflows</text>
  <text x="422" y="238" fill="#ddd8f0" font-size="10" text-anchor="middle">Composer à l'exécution</text>
  <text x="422" y="256" fill="#7874a0" font-size="9" text-anchor="middle">étapes assemblées au runtime</text>
  <rect x="565" y="8" width="175" height="259" rx="8" fill="none" stroke="#2e3250" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="652" y="35" fill="#7874a0" font-size="10" font-weight="600" text-anchor="middle">COMPOSITION</text>
  <text x="652" y="62" fill="#4f8ef7" font-size="10" text-anchor="middle">Augmented LLM = Tools</text>
  <text x="652" y="105" fill="#2dd4a0" font-size="10" text-anchor="middle">Workflow</text>
  <text x="652" y="121" fill="#7874a0" font-size="9" text-anchor="middle">= primitives câblées</text>
  <text x="652" y="155" fill="#a78bfa" font-size="10" text-anchor="middle">Agent</text>
  <text x="652" y="171" fill="#7874a0" font-size="9" text-anchor="middle">= modèle choisit</text>
  <text x="652" y="210" fill="#4f8ef7" font-size="10" text-anchor="middle">Multi-agent</text>
  <text x="652" y="226" fill="#7874a0" font-size="9" text-anchor="middle">= Orchestrator</text>
  <text x="652" y="242" fill="#7874a0" font-size="9" text-anchor="middle">+ Subagents</text>
</svg>
:::

:::rule
**Parcimonie :** minimum de primitives. Chaque ajout = latence + tokens + surface à gouverner.
:::

## Sélection de modèles

### Les 3 patterns

:::mindmap
<svg viewBox="0 0 820 380" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif">
  <line x1="70" y1="330" x2="760" y2="330" stroke="#2e3250" stroke-width="1.5"/>
  <line x1="70" y1="330" x2="70" y2="30" stroke="#2e3250" stroke-width="1.5"/>
  <polygon points="760,326 770,330 760,334" fill="#2e3250"/>
  <polygon points="66,30 70,20 74,30" fill="#2e3250"/>
  <text x="415" y="358" fill="#7874a0" font-size="11" text-anchor="middle">PREDICTABILITE →</text>
  <text x="22" y="180" fill="#7874a0" font-size="11" text-anchor="middle" transform="rotate(-90,22,180)">AUTONOMIE →</text>
  <rect x="82" y="40" width="220" height="120" rx="8" fill="#1c1f2e" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="192" y="68" fill="#a78bfa" font-size="13" font-weight="bold" text-anchor="middle">AGENT</text>
  <text x="192" y="88" fill="#ddd8f0" font-size="10" text-anchor="middle">Autonomie elevee</text>
  <text x="192" y="104" fill="#ddd8f0" font-size="10" text-anchor="middle">Trajectoire imprevisible</text>
  <text x="192" y="120" fill="#7874a0" font-size="9" text-anchor="middle">Le modele controle le flux</text>
  <text x="192" y="148" fill="#f87171" font-size="9" text-anchor="middle">Cout · Latence · Audit</text>
  <rect x="295" y="160" width="230" height="110" rx="8" fill="#1c1f2e" stroke="#2dd4a0" stroke-width="1.5"/>
  <text x="410" y="186" fill="#2dd4a0" font-size="13" font-weight="bold" text-anchor="middle">WORKFLOW</text>
  <text x="410" y="206" fill="#ddd8f0" font-size="10" text-anchor="middle">Forme previsible</text>
  <text x="410" y="222" fill="#ddd8f0" font-size="10" text-anchor="middle">Jugement delimite par etape</text>
  <text x="410" y="238" fill="#7874a0" font-size="9" text-anchor="middle">Votre code controle le flux</text>
  <text x="410" y="256" fill="#2dd4a0" font-size="9" text-anchor="middle">Observable · Testable</text>
  <rect x="525" y="250" width="225" height="65" rx="8" fill="#1c1f2e" stroke="#4f8ef7" stroke-width="1.5"/>
  <text x="637" y="272" fill="#4f8ef7" font-size="13" font-weight="bold" text-anchor="middle">AUGMENTED LLM</text>
  <text x="637" y="290" fill="#ddd8f0" font-size="10" text-anchor="middle">Un seul appel delimite</text>
  <text x="637" y="306" fill="#7874a0" font-size="9" text-anchor="middle">Peut inclure Tools / RAG</text>
</svg>
:::

### Arbre de décision — quel pattern choisir ?

:::mermaid
flowchart TD
  Q1{Etapes previsibles ?} -- Non --> AG[Agent]
  Q1 -- Oui --> Q2{Cout erreur eleve ?}
  Q2 -- Oui --> WF[Workflow]
  Q2 -- Non --> Q3{Observabilite requise ?}
  Q3 -- Oui --> WF2[Workflow]
  Q3 -- Non --> Q4{Latence ou tokens critiques ?}
  Q4 -- Oui --> AL[Augmented LLM]
  Q4 -- Non --> WF3[Workflow]
  style AG fill:#1c1f2e,stroke:#a78bfa,color:#ddd8f0
  style WF fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style WF2 fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style WF3 fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style AL fill:#1c1f2e,stroke:#4f8ef7,color:#ddd8f0
:::

:::rule
**Erreur fréquente :** choisir Agent parce que la tâche "semble ouverte". Si les étapes sont connaissables à l'avance → **Workflow**.
:::

### Les 4 sous-patterns du Workflow

:::mermaid
flowchart TB
  subgraph Chaining
    direction LR
    c1[Extraire] --> c2[Classifier] --> c3[Synthétiser]
  end
  subgraph Routing
    direction LR
    r0[Input] --> r1{Type ?}
    r1 -->|Billing| r2[Agent billing]
    r1 -->|Tech| r3[Doc tech]
    r1 -->|Escalade| r4[Humain]
  end
  subgraph Parallelization
    direction LR
    p1[Contrat 1] --> p4[Synthese]
    p2[Contrat 2] --> p4
    p3[Contrat N] --> p4
  end
  subgraph EvaluatorOptimizer
    direction LR
    e1[Generer] --> e2{OK ?}
    e2 -->|Non| e1
    e2 -->|Oui| e3[Output]
  end
:::

:::flashcards
Q: Quand utiliser Evaluator-Optimizer plutôt que Chaining ?
R: Quand la qualité est **vérifiable** mais une seule tentative n'est pas fiable. Ex : code + suite de tests.

Q: Agent vs Workflow — différence fondamentale ?
R: **Flux de contrôle** — Workflow : votre code. Agent : le modèle. L'agent échoue silencieusement, le Workflow avec une erreur déboguable.

Q: Evaluator-Optimizer — quand le préférer à un simple Chaining ?
R: Quand la qualité est **vérifiable objectivement** (tests, critères) et qu'une seule passe est insuffisante.

Q: Fine-tuning — quand est-ce justifié selon Anthropic ?
R: En **dernier recours** — après avoir épuisé prompting, tools et Workflows. Disponibilité limitée sur Claude.
:::

## Systèmes multi-agents

### Architecture Fan-out

:::mermaid
flowchart TD
  O[Orchestrator] --> S1[Sub-agent 1]
  O --> S2[Sub-agent 2]
  O --> S3[Sub-agent N]
  S1 --> R[Synthese]
  S2 --> R
  S3 --> R
  style O fill:#1c1f2e,stroke:#4f8ef7,color:#ddd8f0
  style S1 fill:#1c1f2e,stroke:#a78bfa,color:#ddd8f0
  style S2 fill:#1c1f2e,stroke:#a78bfa,color:#ddd8f0
  style S3 fill:#1c1f2e,stroke:#a78bfa,color:#ddd8f0
  style R fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
:::

### Récupérabilité des défaillances

:::mermaid
flowchart LR
  F1[Sub-agent echoue] -- Recuperable --> A1[Relancer ou Rediriger]
  F2[Orchestrator echoue] -- Irrecuperable --> A2[Execution perdue]
  style F1 fill:#1c1f2e,stroke:#fbbf24,color:#ddd8f0
  style F2 fill:#1c1f2e,stroke:#f87171,color:#ddd8f0
  style A1 fill:#1c1f2e,stroke:#2dd4a0,color:#ddd8f0
  style A2 fill:#1c1f2e,stroke:#f87171,color:#ddd8f0
:::

:::rule
**Contrôle de couverture :** résultats reçus == unités envoyées. Signaler l'écart **avant** synthèse.
:::

:::situation
**Audit contractuel — 50 sections, 2 unités tombées :**
- Orchestrator synthétise "48 sections examinées" sans contrôle de couverture
- Résumé fluide et confiant → personne ne détecte les 2 manquantes
- Transmis au responsable juridique comme complet
:::

:::flashcards
Q: Asymétrie Orchestrator vs Sub-agent — laquelle est récupérable ?
R: **Sub-agent** (relancer). **Orchestrator** : souvent irrécupérable — il détient l'objectif et la synthèse.

Q: Pourquoi un résumé fluide est dangereux dans un Fan-out ?
R: Il **masque les unités manquantes**. La confiance apparente empêche de détecter les défaillances silencieuses.

Q: Contrôle de couverture Fan-out — quand l'effectuer ?
R: **Avant** la synthèse — vérifier que résultats reçus == unités envoyées. Sinon signaler l'écart.

Q: Orchestrator vs Sub-agent — qui détient l'objectif global ?
R: L'**Orchestrator** — sa défaillance est donc souvent irrécupérable contrairement à un sub-agent.
:::
