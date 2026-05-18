# PROJECT_STATUS.md — k2000_visa_generator

Snapshot architektury i stanu projektu (po refactoringu `lib_code/` → `app/` i przejściu na wzorzec `wsgi.py` + `WebApp`).
To opis tego co **JEST** — nie historia zmian.

---

## Stack

- **Backend:** Python 3.13+ · Flask 3.x · Jinja2 · Gunicorn
- **Pakiety:** uv (`pyproject.toml` + `uv.lock`, jedyna obsługiwana metoda)
- **Konteneryzacja:** Docker multi-stage (python-deps → runtime), GHCR
- **CI/CD:** GitHub Actions, trigger na tagi `v*`

---

## Layout repozytorium

```
wsgi.py                       # bootstrap: init_app() + WebApp(is_debug) + re-export `app` dla gunicorna
run.py                        # CLI: wygenerowanie kodu bez startowania serwera
app/
├── WebApp.py                 # klasa Flask app: rejestruje /, /generate, context processor
├── PhilipsGenerator.py       # fasada generatora
├── Computer.py               # kompozycja transformacji
├── DeviceIdParser.py         # parser stringa device_id
├── TimeHelper.py             # datetime → Windows FILETIME
├── Transform.py              # SeedTransform + TimeTransform + Transform1/2 (RE)
├── Uint32.py / Uint64.py     # emulacja arytmetyki unsigned C
├── helpers/
│   └── config_builder.py     # init_app(): logging + .logs/
└── templates/
    └── index.html            # formularz + JSON fetch /generate

config/
└── logging.yaml              # rotujące logi: .logs/app_info.log + .logs/generated_codes.log

static/
├── favicon/                  # favicon set
└── k2000.jpg                 # baner

docker/
├── Dockerfile                # multi-stage uv (deps + runtime python:3.13-slim)
├── build.sh                  # lokalny build z logiem + auto-bump
├── release.sh                # bump + commit + tag + push (trigger GitHub Actions)
├── build_utils.py            # get_version / inc_version / get_build_time
└── _ver.txt                  # MAJOR.MINOR.PATCH.BUILD

tests/                        # unit-testy z konkretnymi wartościami referencyjnymi (RE)

.github/workflows/docker.yml  # trigger v*: build + push do ghcr.io/robertolechowski/k2000-visa-generator
```

---

## Wzorzec architektoniczny

- **Klasa `WebApp`** (uproszczona wersja wzorca z `robertolechowski.com`): trzyma instancję Flaska + generatora, rejestruje endpointy i context processor.
- Aplikacja jest mała (2 endpointy), więc nie używa `BaseController`/`Blueprint` z `rotools`. Jeśli urośnie — refactor wg wzorca z `robertolechowski.com/docs/CLAUDE.md`.

---

## Kontekst dla szablonów (context processor `_inject_globals`)

W każdym renderze dostępne są:

- `app_version` — z env `RR_BUILD_VERSION` (Docker ARG), `"DEBUG"` w devie.
- `is_debug` — `app.debug`
- `year` — `datetime.now().year`

---

## Docker / runtime

**Multi-stage:**

1. `python-deps` (`python:3.13-slim`) — `uv sync --frozen --no-dev --no-install-project` z cache mount.
2. **Runtime** (`python:3.13-slim`) — kopiowane:
   - `.venv` z `python-deps`
   - `app/`, `config/`, `static/`, `wsgi.py`
   - **Brak** uv binary, brak cache.

**Wersjonowanie:** `BUILD_VERSION` przekazywany jako ARG → env `RR_BUILD_VERSION`. Czytany w `_inject_globals`.

**Uruchomienie:** `gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 1 --no-control-socket wsgi:app`.

**Użytkownik:** `appuser` (UID 1000, GID 1000); chmod `g+rwX` dla grupy 0 — pozwala uruchomić pod dowolnym UID-em w grupie 0.

---

## Co działa, czego brakuje

**Działa:**
- `/` (formularz), `/generate` (POST → JSON z kodem)
- CLI: `python run.py` (przykład generowania kodu)
- Testy `tests/test_*.py` z wartościami referencyjnymi (RE)
- Auto-bump wersji w `docker/release.sh` + GitHub Actions deploy do GHCR

**Otwarte zadania:** `docs/PLAN.md`.

---

## Konwencje (skrót — pełne w `docs/CLAUDE.md`)

- Język kodu: angielski. Polski tylko w wartościach widocznych dla użytkownika.
- Brak docstringów i komentarzy opisujących oczywisty przepływ.
- Logika reverse-engineeringu (`Transform.py`) — nie zmieniać bez pełnego pokrycia testami.
- Nowy endpoint = nowa metoda w `WebApp` + rejestracja w `_register_routes`.
