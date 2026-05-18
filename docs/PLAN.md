# PLAN.md — k2000_visa_generator

Lista otwartych zadań (`[ ]`). AI usuwa zrealizowane.

---

## Backend / generator

- [ ] **Dodać wsparcie dla innych modeli CT** (poza Philips). Wymaga rozpoznania algorytmu — research RE.
- [ ] **Walidacja długości `days`** w endpoincie `/generate` — obecnie hardcoded 5, ale logika `PhilipsGenerator.generate` przyjmuje parametr. Dodać input w UI i walidację (1..365).

---

## Frontend / UX

- [ ] **Wyświetlić wersję w stopce** — `app_version` jest już w context processor, dodać render w `index.html`.
- [ ] **Favicon set** — sprawdzić czy `static/favicon/*` istnieje (template'a używa).

---

## DevOps / build

- [ ] **uv.lock w repo** — wygenerować przez `uv sync` i zacommitować (`uv.lock` jest wymagany przez `Dockerfile`: `uv sync --frozen`).

