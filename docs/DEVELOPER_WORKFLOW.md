# 🚀 Developer Workflow Guide

Professioneller Entwicklungsworkflow für FastAPI-Anwendung mit Docker, Git und CI/CD.

## 📋 Übersicht

Dieser Workflow zeigt dir, wie Profis neue Features entwickeln - von der ersten Idee bis zur Production.

---

## 🔄 **KOMPLETTER FEATURE-ENTWICKLUNGS-WORKFLOW**

### **Phase 1: Vorbereitung & Setup**

#### 1.1 Feature Branch erstellen
```bash
# Neue Feature Branch vom main-Branch erstellen
git checkout main
git pull origin main
git checkout -b feature/user-authentication

# Naming Convention:
# feature/feature-name    - Neue Features
# bugfix/bug-description  - Bugfixes
# hotfix/critical-fix     - Kritische Hotfixes
```

#### 1.2 Docker Development Environment starten
```bash
# Docker Development Container starten
docker-compose up --build

# Was passiert:
# - Build development image mit Hot-Reload
# - Startet Container auf Port 8000
# - Mount current directory -> Live Code Changes
# - Auto-Reload bei Code-Änderungen
```

**🌐 Verfügbare URLs:**
- **API Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

### **Phase 2: Development Loop**

#### 2.1 Code schreiben
```bash
# Beispiel: Neuen User Endpoint entwickeln

# 1. Models definieren (src/fast_api/models.py)
# 2. Endpoint implementieren (src/fast_api/routers/api.py)
# 3. Tests schreiben (tests/test_api.py)
```

#### 2.2 Live Testing
```bash
# Container läuft bereits -> Änderungen sind sofort sichtbar!
# Browser: http://localhost:8000/docs
# - Swagger UI zeigt neue Endpoints
# - Direkt testen möglich
# - Änderungen in Echtzeit sichtbar
```

#### 2.3 Tests ausführen (während Development)
```bash
# Tests im Docker Container
docker-compose exec app uv run pytest

# Oder lokal (wenn UV installiert)
uv run pytest

# Mit Coverage
uv run pytest --cov=src --cov-report=html
```

#### 2.4 Code Quality prüfen
```bash
# Linting
uv run ruff check .
uv run ruff format .

# Type Checking
uv run mypy src/

# Oder alles zusammen
uv run pre-commit run --all-files
```

---

### **Phase 3: Integration & Testing**

#### 3.1 Commit mit Pre-commit Hooks
```bash
git add .
git commit -m "feat: add user authentication endpoints

- Add User model with validation
- Implement POST /users and GET /users/{id}
- Add comprehensive tests
- Update API documentation"

# Was passiert automatisch:
# ✅ Pre-commit hooks laufen
# ✅ Code wird auto-formatiert
# ✅ Linting wird ausgeführt
# ✅ Type-Checking wird gemacht
# ⚠️ Bei Fehlern: Commit wird abgebrochen
```

#### 3.2 Push Feature Branch
```bash
git push origin feature/user-authentication

# Was passiert:
# - Branch wird auf GitHub gepushed
# - Noch KEINE CI/CD Pipeline (nur bei main/develop)
# - Bereit für Pull Request
```

---

### **Phase 4: Pull Request & Review**

#### 4.1 Pull Request erstellen
```bash
# Auf GitHub:
# 1. "Compare & pull request" Button
# 2. PR Title: "feat: Add user authentication"
# 3. Beschreibung mit Details
# 4. Reviewer zuweisen
# 5. Labels setzen (enhancement, api, etc.)
```

**📝 PR Template:**
```markdown
## 🎯 Was wurde implementiert?
- User authentication endpoints
- Input validation with Pydantic
- Comprehensive test coverage

## 🧪 Wie getestet?
- [x] Unit Tests (pytest)
- [x] Integration Tests
- [x] Manual Testing in Swagger UI
- [x] Code Coverage > 90%

## 📋 Checklist
- [x] Tests hinzugefügt/aktualisiert
- [x] Dokumentation aktualisiert
- [x] Pre-commit hooks bestanden
- [x] Breaking Changes: Nein
```

#### 4.2 Review Process
```bash
# Reviewer macht:
# 1. Code Review im Browser
# 2. Feedback/Änderungswünsche
# 3. Approve oder Request Changes
```

---

### **Phase 5: Merge & Deployment**

#### 5.1 Merge in Main Branch
```bash
# Nach Approval:
git checkout main
git pull origin main
git merge feature/user-authentication
git push origin main

# Oder: Squash & Merge via GitHub UI (empfohlen)
```

#### 5.2 CI/CD Pipeline startet automatisch
```yaml
# Was passiert beim Push auf main:

📦 Test Job:
  ✅ Dependencies installieren
  ✅ Ruff Linting
  ✅ MyPy Type-Checking
  ✅ Pytest mit Coverage
  ✅ Coverage Report hochladen

🔒 Security Job:
  ✅ Bandit Security Scan
  ✅ Dependency Vulnerability Check

🐳 Docker Job:
  ✅ Production Image bauen
  ✅ Image zu GitHub Container Registry pushen
  ✅ Tags: latest + commit-sha

🚀 Deploy Job:
  ✅ Production Deployment
  ✅ Health Checks
  ✅ Rollback bei Fehlern
```

#### 5.3 Production Deployment
```bash
# Automatisch deployed:
# - Neue Docker Image wird deployed
# - Health Checks werden ausgeführt
# - Bei Fehlern: Automatic Rollback
# - Monitoring & Alerts aktiv
```

---

### **Phase 6: Cleanup**

#### 6.1 Feature Branch löschen
```bash
# Lokal löschen
git branch -d feature/user-authentication

# Remote löschen (oder via GitHub UI)
git push origin --delete feature/user-authentication
```

#### 6.2 Docker Environment cleanup
```bash
# Container stoppen
docker-compose down

# Bei Bedarf: Images aufräumen
docker system prune
```

---

## 🔚 **END-OF-SESSION WORKFLOW**

### **Coding Session sauber beenden - Schritt für Schritt**

Wenn du mit dem Coden fertig bist, solltest du immer diese **Cleanup-Routine** durchführen:

#### **Schritt 1: Arbeit sichern** 💾
```bash
# Alle Änderungen committen (falls noch nicht geschehen)
git status
git add .
git commit -m "wip: save current progress"

# Optional: Push to backup current work
git push origin feature/your-branch
```

#### **Schritt 2: Docker Container stoppen** 🐳
```bash
# Sauber stoppen (empfohlen)
docker-compose down

# Was passiert:
# ✅ Container werden gestoppt
# ✅ Netzwerke werden entfernt
# ✅ Volumes bleiben erhalten
# ✅ Images bleiben erhalten (für nächste Session)

# Alternative: Nur Container stoppen (für temporäre Pause)
# docker-compose stop
```

#### **Schritt 3: Workspace aufräumen** 🧹
```bash
# Browser-Tabs schließen:
# - http://localhost:8000/docs
# - http://localhost:8000
# - GitHub PR/Issues

# IDE/Editor schließen oder Projekt schließen
# Terminal-Tabs aufräumen
```

#### **Schritt 4: System-Ressourcen prüfen** 📊
```bash
# Optional: Docker-Ressourcen checken
docker system df

# Bei viel ungenutztem Speicher (optional cleanup):
# docker system prune

# Container-Status checken
docker ps -a
```

#### **Schritt 5: Session dokumentieren** 📝
```bash
# Optional aber empfohlen:
# - TODO-Liste für nächste Session
# - Notizen zu aktuellen Problemen
# - Links zu relevanten Docs/Issues

# Beispiel: Session-Notes erstellen
echo "## Session $(date +%Y-%m-%d)" >> SESSION_NOTES.md
echo "- Implemented: user authentication" >> SESSION_NOTES.md
echo "- TODO: add password hashing" >> SESSION_NOTES.md
echo "- Issues: validation edge cases" >> SESSION_NOTES.md
```

---

### **🚀 NÄCHSTE SESSION STARTEN**

Wenn du wieder anfängst zu coden:

#### **Quick Start (Normal)**
```bash
# 1. Repository aktuelle Version holen
git checkout main
git pull origin main

# 2. Zu deiner Feature Branch wechseln
git checkout feature/your-branch

# 3. Docker Environment starten
docker-compose up --build

# 4. Browser öffnen
# - http://localhost:8000/docs
```

#### **Clean Start (Bei Problemen)**
```bash
# Falls Docker-Probleme:
docker-compose down
docker system prune -f
docker-compose up --build --force-recreate
```

---

### **💡 SESSION MANAGEMENT TIPPS**

#### **Für längere Pausen (> 1 Stunde):**
```bash
# Vollständiges Cleanup empfohlen
docker-compose down
docker system prune

# Warum?
# ✅ Spart RAM/CPU
# ✅ Verhindert Port-Konflikte
# ✅ Cleaner System-Status
```

#### **Für kurze Pausen (< 30 Min):**
```bash
# Container können laufen bleiben
# Einfach Browser-Tab minimieren
# Docker läuft im Hintergrund weiter

# Oder pausieren:
docker-compose stop
# Und später:
docker-compose start
```

#### **Für Laptop-Shutdown:**
```bash
# IMMER vor dem Herunterfahren:
docker-compose down

# Warum?
# ✅ Verhindert corrupted containers
# ✅ Sauberer System-Start
# ✅ Keine zombie processes
```

#### **Für Wechsel zwischen Projekten:**
```bash
# Aktuelles Projekt sauber beenden
docker-compose down
cd ../other-project

# Neues Projekt starten
docker-compose up

# Port-Konflikte vermeiden!
```

---

### **🚨 TROUBLESHOOTING: SESSION-PROBLEME**

#### **"Port 8000 bereits belegt":**
```bash
# Zombie-Container killen
docker-compose down
docker ps -a
docker rm $(docker ps -aq)

# Oder Port-Prozess killen
lsof -ti:8000 | xargs kill -9
```

#### **"Container startet nicht":**
```bash
# Logs checken
docker-compose logs app

# Vollständiger Reset
docker-compose down
docker system prune -f
docker-compose up --build --force-recreate
```

#### **"Git-Probleme beim Sessionende":**
```bash
# Uncommitted changes sichern
git stash
# Oder
git add . && git commit -m "wip: session end"

# Branch-Status prüfen
git status
git branch
```

---

### **📋 SESSION-END CHECKLISTE**

**Vor jedem Session-Ende:**
- [ ] Alle Änderungen committed oder gestashed
- [ ] Docker containers gestoppt (`docker-compose down`)
- [ ] Browser-Tabs geschlossen
- [ ] IDE/Editor saved & closed
- [ ] TODO-Liste für nächste Session (optional)
- [ ] Terminal aufgeräumt

**Bei längerem Pause (> 1 Tag):**
- [ ] Branch auf GitHub gepushed (backup)
- [ ] Docker cleanup (`docker system prune`)
- [ ] Notizen zu aktueller Arbeit
- [ ] Issues/PRs auf GitHub gecheckt

**Bei Projekt-Wechsel:**
- [ ] Current project: `docker-compose down`
- [ ] Port-Konflikte prüfen
- [ ] Directory wechseln
- [ ] New project: Setup routine

---

---

## 🔄 **DEVELOPMENT-OPTIONEN**

### **Option A: Docker Development (Empfohlen)**
```bash
# Pros:
✅ Konsistente Umgebung
✅ Gleich wie Production
✅ Keine lokale Python-Installation nötig
✅ Hot-Reload funktioniert
✅ Port-Isolation

# Cons:
❌ Etwas langsamer beim Starten
❌ Mehr RAM-Verbrauch
```

### **Option B: Lokale Development**
```bash
# Pros:
✅ Schneller Start
✅ Weniger Ressourcen
✅ Native IDE-Integration

# Cons:
❌ Python/UV muss lokal installiert sein
❌ Potentielle Umgebungsunterschiede
```

---

## 🚨 **WICHTIGE WORKFLOWS**

### **Hotfix Workflow (Kritische Bugfixes)**
```bash
# 1. Hotfix Branch von main
git checkout main
git checkout -b hotfix/critical-security-fix

# 2. Fix implementieren & testen
# 3. Direkt in main mergen (bypasses normal review)
# 4. Tag erstellen
git tag -a v1.0.1 -m "Hotfix: Security vulnerability"

# 5. Deploy läuft automatisch
```

### **Release Workflow**
```bash
# 1. Release Branch
git checkout -b release/v1.1.0

# 2. Version Updates, Final Testing
# 3. Merge in main + develop
# 4. Tag erstellen
git tag -a v1.1.0 -m "Release v1.1.0"
```

---

## 📊 **MONITORING & FEEDBACK**

### **Was passiert nach dem Deployment:**
- 📈 **Monitoring**: Metriken werden gesammelt
- 🚨 **Alerts**: Bei Fehlern/Performance-Issues
- 📊 **Analytics**: API-Usage wird getrackt
- 🔍 **Logging**: Zentrale Log-Aggregation
- 💬 **User Feedback**: Issue-Tracking

### **Rollback bei Problemen:**
```bash
# Automatisch bei:
❌ Health Check Failures
❌ Error Rate > 5%
❌ Response Time > 2s

# Manuell:
kubectl rollout undo deployment/fast-api
```

---

## 🎯 **BEST PRACTICES**

### **Branch Naming:**
- `feature/user-auth` - Neue Features
- `bugfix/login-error` - Bugfixes
- `hotfix/security-patch` - Kritische Fixes
- `refactor/api-structure` - Code-Refactoring

### **Commit Messages:**
```bash
feat: add user authentication endpoint
fix: resolve login validation error
docs: update API documentation
test: add integration tests for auth
refactor: improve error handling
```

### **PR Best Practices:**
- 🎯 **Klein & Fokussiert**: Ein Feature pro PR
- 📝 **Gute Beschreibung**: Was, Warum, Wie
- 🧪 **Tests**: Immer Tests hinzufügen
- 📚 **Docs**: Dokumentation aktualisieren
- 🏷️ **Labels**: Proper Tagging

---

## 🆘 **TROUBLESHOOTING**

### **Docker Issues:**
```bash
# Container startet nicht:
docker-compose logs app

# Port bereits belegt:
docker-compose down
lsof -ti:8000 | xargs kill -9

# Image rebuild:
docker-compose up --build --force-recreate
```

### **Git Issues:**
```bash
# Merge Conflicts:
git status
# Konflikte lösen
git add .
git commit

# Reset zu letztem Commit:
git reset --hard HEAD~1
```

### **CI/CD Issues:**
- 🔍 **GitHub Actions Tab**: Pipeline-Logs checken
- 🐳 **Docker Build Fails**: Dockerfile prüfen
- 🧪 **Tests Fail**: Lokal reproduzieren
- 🔒 **Security Issues**: Bandit-Report analysieren

---

## 📚 **WEITERFÜHRENDE RESOURCEN**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Git Flow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [GitHub Actions CI/CD](https://docs.github.com/en/actions)

---

*Dieser Workflow wird kontinuierlich aktualisiert basierend auf Team-Feedback und Best Practices.*
