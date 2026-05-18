# k2000_visa_generator — Configuration & Guidelines

> [!IMPORTANT]
> **Ten plik (`docs/CLAUDE.md`) jest źródłem prawdy** dla wszystkich agentów AI pracujących nad projektem.
> `CLAUDE.md` w korzeniu projektu to cienki wrapper odsyłający tutaj.
> Wszystkie zmiany konfiguracji wprowadzaj w tym pliku.

## Quick Start (TL;DR dla agenta)

1. Przeczytaj `docs/PLAN.md` (jeśli istnieje) → znajdź pierwszy `[ ]` na liście.
2. Zrób PoC → wypisz zmienione pliki → czekaj na vibe check.
3. Po akceptacji: lokalny smoke test (`uv run python wsgi.py`, ręczny check w przeglądarce) → zaktualizuj `PROJECT_STATUS.md` jeśli istnieje.
4. Zapytaj o commit — **nigdy nie commituj samodzielnie**.

Szczegółowy workflow → sekcja "Zasady pracy agenta" poniżej.

---

## Zasady pracy agenta

### Workflow iteracyjny

**Podstawowe kroki (zawsze):**

1. Przeczytaj `docs/PLAN.md` (jeśli istnieje) — znajdź pierwszy krok `[ ]` (nie zrobiony).
2. Wykonaj go metodą **Dirty-First**: najmniejszy działający PoC, pokaż użytkownikowi. Czekaj na vibe check.
3. Po akceptacji: smoke test → zaktualizuj `PROJECT_STATUS.md` (jeśli istnieje).
4. **Dopiero po kroku 3:** Zapytaj czy commit. Jeśli tak — przygotuj zwięzły message i commituj. **STOP** — czekaj na feedback.

**Opcjonalnie (gdy dotyczy):**
- Zadaj pytania o nadchodzące decyzje **tylko jeśli droga do PoC była niejednoznaczna** — maks. 3 pytania w formacie A/B/C.

### Aktualizacja dokumentacji przy commicie

Gdy użytkownik potwierdza commit, **przed** wykonaniem `git commit` zaktualizuj automatycznie (jeśli plik istnieje):

1. **`docs/PLAN.md`** — upewnij się, że krok jest oznaczony `[x]` lub usunięty z listy otwartych.
2. **`docs/PROJECT_STATUS.md`** — zaktualizuj snapshot: co działa, jakie moduły zmienione, jakie nowe ścieżki.
3. **`docs/CLAUDE.md`** — zaktualizuj jeśli zmieniła się architektura, stack lub zasady.

Nie pytaj o zgodę na aktualizację dokumentacji — to obowiązkowy krok przed każdym commitem.

### Aktualizacja CLAUDE.md przy zmianie stylu/techniki

Gdy użytkownik wydaje polecenie dotyczące stylu, techniki lub frameworka (np. "używaj X zamiast Y", "zawsze rób Z"), zapytaj:
> "Czy mam zaktualizować `docs/CLAUDE.md` o tę zasadę, żeby obowiązywała w przyszłych sesjach?"

### Dirty-First — prototypowanie

Przed pełną implementacją **zawsze** produkuj minimalny działający PoC:

**Faza 1: PoC (bez polerowania)**
- Kod bez pełnych docstringów, możliwe hardcoded wartości — to jest OK.
- Pokaż użytkownikowi: wypisz zmienione pliki, pokaż kluczowe fragmenty. Czekaj na vibe check.

**Faza 2: Po vibe check — cleanup**
- Smoke test (uruchom `uv run python wsgi.py`, wejdź na `/` i sprawdź generowanie kodu).
- Oznacz krok jako `[x]` w `PLAN.md`, zaktualizuj `PROJECT_STATUS.md` (jeśli istnieją).
- **Potem:** zapytaj użytkownika czy commit. Czekaj na jawną odpowiedź — **nigdy nie commituj samodzielnie**.

**Wyjątek — oczywiste zmiany (od razu czysto, bez PoC):**
- Rename zmiennej/funkcji (bez zmiany zachowania)
- Dodanie/usunięcie importu
- Poprawka 1-linijkowa (typo, błędny operator)
- Aktualizacja wartości w config/YAML (bez zmian logiki)

### Vibe Rules — styl komunikacji

- Jeśli użytkownik pisze **"robimy to"** lub **"zrób"** — działaj bez pytania o potwierdzenie.
- **Wyjątek:** jeśli "zrób X" wymaga decyzji architektonicznej, zadaj **max 3 pytania A/B/C** zanim zaczniesz.
- Jeśli widzisz błąd w logice użytkownika — zaproponuj poprawkę **w jednym zdaniu**, nie przerywaj pracy.
- Pytania decyzyjne zawsze jako **A/B/C** — nigdy otwarte "co myślisz?".
- "Vibe check" = jawna akceptacja użytkownika (OK/Super/tak).
- Odpowiedzi trzymaj zwięźle; długie wyjaśnienia tylko gdy użytkownik pyta.

### Co czytać przy starcie sesji

- **Zawsze:** `docs/CLAUDE.md` (ten plik), `docs/PLAN.md` (jeśli istnieje).
- **Na żądanie:** `docs/PROJECT_STATUS.md` (jeśli istnieje).
- **Nigdy automatycznie:** `docs/private/` (jeśli istnieje).
- **Zasada:** nie czytaj pliku jeśli nie jest potrzebny do wykonywanego kroku.

### Pliki użytkownika — nie edytować bez polecenia

- **`README.md`** — notatki użytkownika. Plik jest **do edycji wyłącznie przez użytkownika**.
  Agent może go czytać, ale **nigdy nie modyfikuje** bez wyraźnego polecenia.
- `docs/private/` — analogicznie, nie czytane ani nie pisane bez polecenia.

### Zarządzanie dokumentacją

- `docs/PLAN.md` — lista otwartych zadań `[ ]` + znane problemy. AI usuwa zrealizowane zadania i aktualizuje problemy.
- `docs/PROJECT_STATUS.md` — snapshot aktualnego stanu: architektura, moduły, decyzje. Nie historia — opis tego co JEST.
- `docs/private/` — prywatne notatki użytkownika — AI czyta/zapisuje TYLKO gdy explicite zlecone.

---

## Project Overview

**k2000_visa_generator** — Flask web app generująca service access codes dla urządzeń medycznych Philips CT (algorytm zreverse-engineerowany z aplikacji "2000 Visa Entry"). Mała aplikacja, jedna strona, jeden endpoint POST `/generate`. [Live Demo](https://codes.robertolechowski.com/)

**Stack:** Python 3.13+ (uv) · Flask 3.x · Jinja2 · Gunicorn · Docker (multi-stage uv)

**Charakter pracy:** sporadyczne dodawanie wsparcia dla nowych modeli CT, utrzymanie pipeline'u build/deploy.

---

## Architecture

### Punkt wejścia
- `wsgi.py` — bootstrap; woła `init_app()` (konfiguracja logów) i tworzy `WebApp(is_debug)`. Re-eksportuje `app = _web_app.app` dla gunicorna (`gunicorn wsgi:app`).
- `app/WebApp.py` — klasa `WebApp` buduje `Flask`, rejestruje endpointy (`/`, `/generate`) i context processor (`app_version`, `is_debug`, `year`). `app_version` pochodzi z env `RR_BUILD_VERSION` (ustawiane w Docker build), w devie = `"DEBUG"`.
- **Uwaga:** plik `wsgi.py` w roocie i pakiet `app/` są celowo rozdzielone, by uniknąć konfliktu nazw (`app.py` vs pakiet `app/`).

### Logika domenowa (`app/`)
- `PhilipsGenerator.py` — fasada: `generate(dev_id, days, current_time)` → `{code, valid_until}`.
- `Computer.py` — kompozycja transformacji (Seed + Time + Transform1/2).
- `DeviceIdParser.py` — parser stringa `XXXX-XXXX` na `Uint32`.
- `TimeHelper.py` — konwersja datetime → Windows FILETIME (100ns od 1601).
- `Transform.py` — `SeedTransform`, `TimeTransform`, `Transform1`, `Transform2`.
- `Uint32.py`, `Uint64.py` — emulacja arytmetyki C (wrap-around, rot_L/rot_R, shift, xor, add, ...).

### Konfiguracja
- `config/logging.yaml` — RotatingFileHandler do `.logs/app_info.log` + `code_generator` logger pisze do `.logs/generated_codes.log`.
- Ładowanie: `app/helpers/config_builder.py::init_app()` tworzy `.logs/` i ładuje YAML.

### Templates
- `app/templates/index.html` — pojedyncza strona z formularzem (Bootstrap CDN). Po submit POST na `/generate` (JSON), wynik wyświetlany inline.
- Główny `template_folder` Flaska ustawiony na `app/templates` w `WebApp.py` (Flask z `root_path=os.getcwd()`).

### Docker / runtime
- `docker/Dockerfile` — multi-stage:
  1. `python-deps` — `python:3.13-slim` + `uv sync --frozen --no-dev --no-install-project`.
  2. runtime `python:3.13-slim` — kopiuje `.venv`, kod (`app/`, `config/`, `wsgi.py`, `static/`). Wersja przekazana przez `--build-arg BUILD_VERSION` jako env `RR_BUILD_VERSION`.
- `docker/build.sh` — lokalny build z logiem (`docker/build.log`), tag GHCR + auto-bump wersji.
- `docker/release.sh` — bumpuje wersję → commit → tag (`vX.Y.Z.N`) → push → wypisuje link do GitHub Actions.
- `docker/build_utils.py` — `get_version` / `inc_version` / `get_build_time` (czyta `docker/_ver.txt`).
- `docker/_ver.txt` — bieżąca wersja `MAJOR.MINOR.PATCH.BUILD`.
- `.github/workflows/docker.yml` — trigger na tagi `v*`, buduje i pushuje do `ghcr.io/robertolechowski/k2000-visa-generator:latest|<ver>`.
- Runtime: `gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 1 --no-control-socket wsgi:app`.

---

## Code Style & Standards

### Language & Naming
- **Język odpowiedzi asystenta:** polski.
- **Język kodu:** angielski — wszystkie nazwy klas, metod, zmiennych w angielskim.
- **Poziom wyjaśnień:** użytkownik to doświadczony programista — pomijaj wyjaśnienia składni; skup się na architekturze i edge case'ach.

### Comments
- Dodawaj komentarze **wyłącznie** gdy kod jest krytycznie skomplikowany (np. fragmenty z reverse-engineeringu w `Transform.py`).
- **ZAKAZ**: dodawania docstrings, komentarzy z typami, komentarzy opisujących oczywisty przepływ.
- Kod ma być samoopisujący się.

### Libraries & Patterns
- Najpierw sprawdź `pyproject.toml` przed dodaniem nowej zależności (`uv add <pkg>`).
- Nowy endpoint = nowa metoda w `WebApp` zarejestrowana w `_register_routes`. Jeśli aplikacja urośnie do >5 endpointów — rozważ wzorzec BaseController/Blueprint analogiczny do `robertolechowski.com`.
- Logika reverse-engineeringu (transformacje) — **nie zmieniać bez pełnego pokrycia testami**. Testy w `tests/` zawierają konkretne wartości referencyjne.

---

## Local Development

```bash
# Środowisko Python — uv (jedyny obsługiwany sposób)
uv sync                        # instaluje wg pyproject.toml + uv.lock

# Uruchomienie aplikacji (debug)
uv run python wsgi.py          # http://127.0.0.1:5000

# Testy
uv run pytest tests/
```

### Release / deployment

```bash
# Lokalny build dockera (test)
./docker/build.sh

# Release: bump wersji + tag + push → GitHub Actions buduje i pushuje obraz do GHCR
./docker/release.sh
```

Po `release.sh` skrypt wypisze link do uruchomionego GitHub Actions run. Workflow trigerowany jest tagiem `v*`.

### Sekrety
Brak sekretów w repo — aplikacja jest stateless, nie ma DB ani auth.

---

## AI Documentation Sync

- **Source of truth:** `docs/CLAUDE.md` (ten plik).
- `CLAUDE.md` w korzeniu projektu — cienki wrapper, nie edytuj.
