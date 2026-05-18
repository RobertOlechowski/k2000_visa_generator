# PLAN.md — k2000_visa_generator

Lista otwartych zadań (`[ ]`). AI usuwa zrealizowane.

---

## Backend / generator

- [ ] **Dodać wsparcie dla innych modeli CT** (poza Philips). Wymaga rozpoznania algorytmu — research RE.
- [ ] **Walidacja długości `days`** w endpoincie `/generate` — obecnie hardcoded 5, ale logika `PhilipsGenerator.generate` przyjmuje parametr. Dodać input w UI i walidację (1..365).

---

## DevOps / build

- [ ] **Pokrycie testami** — uruchomić `pytest --cov`, sprawdzić % pokrycia, dodać brakujące (zwłaszcza dla `WebApp` endpointów i `DeviceIdParser` edge cases).
- [ ] **Pre-commit hook** — `uv run pytest tests/` jako sanity check przed commitem.

---

## Pomysły większe (ankietowe — wymagają decyzji)

- [ ] **CLI mode** — `run.py` istnieje (CLI generator), ale powiela logikę. Decyzja: zostawić oba interfejsy czy zrobić `python -m app` z subkomendami `serve` / `generate`?
