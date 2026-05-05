# Modelado de Amenazas - Reciclap
## Análisis STRIDE Completo

---

## 1. RESUMEN EJECUTIVO

**Plataforma:** Reciclap - Sistema de gestión de residuos reciclables  
**Nivel de Criticidad:** ALTO  
**Fecha de Análisis:** 2026-05-04  

### Vulnerabilidades Críticas Encontradas: 6

1. ✗ **Credenciales en plaintext** → clients_config.json con API keys
2. ✗ **Sin HTTPS** → Comunicación sin encriptación
3. ✗ **JWT sin validación robusta** → Escalada de privilegios posible
4. ✗ **Acceso a fotos sin auth** → Disclosure de información
5. ✗ **Sin rate limiting** → Denial of Service
6. ✗ **Sin auditoría** → Imposible rastrear cambios maliciosos

---

## 2. ANÁLISIS STRIDE DETALLADO

### 2.1 SPOOFING (Suplantación de Identidad)

| # | Amenaza | Probabilidad | Impacto | Severidad | Mitigación |
|---|---------|-------------|---------|-----------|-----------|
| S1 | Acceso sin autenticar a endpoints | ALTA | CRÍTICA | **🔴 CRÍTICA** | Implementar authentication obligatoria en todos los endpoints |
| S2 | JWT débil/expiración larga | ALTA | CRÍTICA | **🔴 CRÍTICA** | Expiración corta (15 min), refresh tokens, validar firma |
| S3 | Fuerza bruta en login | MEDIA | ALTA | **🟠 ALTA** | Rate limiting, 2FA, lockout temporal tras 5 intentos |
| S4 | Session hijacking | MEDIA | CRÍTICA | **🔴 CRÍTICA** | HTTPS obligatorio, SameSite cookies, HTTP-only flags |

**Código Vulnerable Actual:**
```python
# main.py - Sin validación de autorización
@router.get("/admin/users")
async def get_all_users():
    # Cualquiera puede acceder si tiene un JWT válido
    return db.query(User).all()
```

**Fix Recomendado:**
```python
from fastapi import Depends, HTTPException
from typing import Optional

async def verify_admin(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return user
```

---

### 2.2 TAMPERING (Modificación de Datos en Transito/Reposo)

| # | Amenaza | Probabilidad | Impacto | Severidad | Mitigación |
|---|---------|-------------|---------|-----------|-----------|
| T1 | Datos en tránsito sin encriptación (HTTP) | ALTA | CRÍTICA | **🔴 CRÍTICA** | Implementar HTTPS/TLS 1.2+, redireccionar HTTP → HTTPS |
| T2 | Modificación de payloads JSON | MEDIA | ALTA | **🟠 ALTA** | Validación Pydantic, firmar payloads críticos |
| T3 | Injection (SQL, NoSQL, Command) | MEDIA | CRÍTICA | **🔴 CRÍTICA** | ORM (SQLAlchemy) defensivamente, input sanitization |
| T4 | Corrupción de base de datos | BAJA | CRÍTICA | **🔴 CRÍTICA** | Backups regulares, integridad de DB (checksums) |

**Vulnerabilidad: Conexión SQLite Sin Validación**
```python
# main.py - Posible SQL injection si hay inputs dinámicos
Database = "sqlite:///./reciclap.db"  # Sin validación
```

**Fix:**
```python
from sqlalchemy import text

# Usar parameterized queries SIEMPRE
query = db.query(User).filter(User.email == user_input)  # ✓ Seguro
# NO hacer: query = f"SELECT * FROM users WHERE email = '{user_input}'"  # ✗ Vulnerable
```

---

### 2.3 REPUDIATION (Negación/Falta de Auditoría)

| # | Amenaza | Probabilidad | Impacto | Severidad | Mitigación |
|---|---------|-------------|---------|-----------|-----------|
| R1 | Sin logs de acciones | ALTA | MEDIA | **🟡 MEDIA** | Implementar audit trail (quién, qué, cuándo) |
| R2 | Modificación de servicios sin registro | MEDIA | ALTA | **🟠 ALTA** | Timestamp de cambios, soft deletes, versionado |
| R3 | No se puede revocar acciones | BAJA | MEDIA | **🟡 MEDIA** | Undo mechanism, audit log completo |

**Implementación Sugerida:**
```python
# models/audit.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)  # "create_service", "assign_recycler", etc.
    resource = Column(String)  # "Service", "User"
    resource_id = Column(Integer)
    old_values = Column(JSON)  # {status: "pending"}
    new_values = Column(JSON)  # {status: "assigned"}
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
```

---

### 2.4 INFORMATION DISCLOSURE (Exposición de Datos)

| # | Amenaza | Probabilidad | Impacto | Severidad | Mitigación |
|---|---------|-------------|---------|-----------|-----------|
| ID1 | **API keys en plaintext (.env, config)** | ALTA | CRÍTICA | **🔴 CRÍTICA** | Mover a variables de entorno, rotar ASAP |
| ID2 | Fotos sin autorización accesible | ALTA | MEDIA | **🟡 MEDIA** | Validar ownership, servir con autenticación |
| ID3 | Errores exponen detalles internos | MEDIA | MEDIA | **🟡 MEDIA** | Custom error responses, log interno sin leaks |
| ID4 | Passwords en plaintext en DB | CRÍTICA | CRÍTICA | **🔴 CRÍTICA** | Usar bcrypt, argon2 (no plaintext) |
| ID5 | Tokens en localStorage (XSS) | MEDIA | ALTA | **🟠 ALTA** | Usar HTTP-only cookies en lugar de localStorage |
| ID6 | CORS abierto a todos (\*) | MEDIA | ALTA | **🟠 ALTA** | Especificar dominios permitidos |

**🚨 VULNERABILIDAD CRÍTICA DETECTADA: clients_config.json**

Según el manual anterior, existen credenciales en plaintext:
```json
{
  "groq_api_key": "gsk_...",  // ✗ EXPUESTO
  "openai_api_key": "sk-...",  // ✗ EXPUESTO
  "other_credentials": "..."   // ✗ EXPUESTO
}
```

**ACCIÓN INMEDIATA:**
1. Revocar todas las API keys en el archivo
2. Crear nuevas keys en Groq/OpenAI
3. Mover a `.env` con variables de entorno
4. Agregar `.env` a `.gitignore`

**Implementación Correcta:**
```python
# config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    secret_key: str = os.getenv("SECRET_KEY")
    database_url: str = os.getenv("DATABASE_URL")
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**.env (NO COMMIT A GIT):**
```
GROQ_API_KEY=gsk_nuevo_valor
OPENAI_API_KEY=sk_nuevo_valor
SECRET_KEY=clave-muy-larga-aleatoria
DATABASE_URL=sqlite:///./reciclap.db
```

---

### 2.5 DENIAL OF SERVICE (DoS)

| # | Amenaza | Probabilidad | Impacto | Severidad | Mitigación |
|---|---------|-------------|---------|-----------|-----------|
| D1 | Upload masivo (explosion de storage) | MEDIA | MEDIA | **🟡 MEDIA** | Limitar tamaño archivos (10MB max), cuota por usuario |
| D2 | Requests masivos (CPU exhaustion) | MEDIA | ALTA | **🟠 ALTA** | Rate limiting (ej. 100 req/min por IP) |
| D3 | Queries complejas (DB lock) | BAJA | MEDIA | **🟡 MEDIA** | Query timeouts, índices en DB |

**Implementación Rate Limiting:**
```python
# requirements.txt
slowapi==0.1.8

# main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/services")
@limiter.limit("10/minute")  # Max 10 requests/min por IP
async def create_service(request: Request, service: ServiceCreate):
    return await service_use_case.create(service)
```

---

### 2.6 ELEVATION OF PRIVILEGE (Escalada de Privilegios)

| # | Amenaza | Probabilidad | Impacto | Severidad | Mitigación |
|---|---------|-------------|---------|-----------|-----------|
| E1 | Cliente puede llamar endpoint admin | ALTA | CRÍTICA | **🔴 CRÍTICA** | Validar rol en cada endpoint sensible |
| E2 | Reciclador accede datos de otros | MEDIA | ALTA | **🟠 ALTA** | Filtrar por user_id (row-level security) |
| E3 | Admin modification sin audit | MEDIA | ALTA | **🟠 ALTA** | Audit trail + confirmación 2-step |

**Patrón Vulnerable:**
```python
# ✗ VULNERABLE - No valida rol
@router.get("/api/v1/admin/users")
async def list_all_users(token: str = Depends(oauth2_scheme)):
    # Si el token es válido, acceso otorgado
    return db.query(User).all()
```

**Patrón Seguro:**
```python
# ✓ SEGURO - Valida rol
@router.get("/api/v1/admin/users")
async def list_all_users(current_user: User = Depends(get_current_admin_user)):
    # Solo admin puede acceder
    return db.query(User).all()

async def get_current_admin_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return user
```

---

## 3. MATRIZ DE RIESGO

```
Probabilidad vs Impacto

                   BAJA        MEDIA        ALTA         CRÍTICA
CRÍTICA      ┌─────────┬──────────┬──────────┬──────────┐
             │         │          │    S1    │  S2,ID1  │
             │ ID4,E1  │  T1      │  T3,D2   │  T1,E1   │
             └─────────┴──────────┴──────────┴──────────┘
ALTA         │         │   ID3    │  S4,D2   │  ID2,D1  │
             └─────────┴──────────┴──────────┴──────────┘
MEDIA        │  R3     │   T4     │  R1,R2   │   ID3    │
             └─────────┴──────────┴──────────┴──────────┘
BAJA         │         │          │   D3     │          │
             └─────────┴──────────┴──────────┴──────────┘

Zona ROJA (Crítica Alto Riesgo): S1, S2, ID1, ID4, E1, T1
```

---

## 4. PLAN DE MITIGACIÓN (ROADMAP)

### **Fase 1: INMEDIATA (Esta Semana)**
- [ ] Revocar y rotar API keys en clients_config.json
- [ ] Mover credenciales a .env
- [ ] Agregar .env a .gitignore
- [ ] Implementar validación de rol en endpoints admin

### **Fase 2: CORTO PLAZO (1-2 Semanas)**
- [ ] Implementar HTTPS (self-signed en dev, Let's Encrypt en producción)
- [ ] Añadir rate limiting (slowapi)
- [ ] Implementar audit trail (AuditLog model)
- [ ] Validación de acceso a fotos (auth + ownership)

### **Fase 3: MEDIANO PLAZO (2-4 Semanas)**
- [ ] Implementar refresh tokens
- [ ] Añadir 2FA opcional para admin
- [ ] Mejorar validación de inputs (Pydantic)
- [ ] Sanitizar errores HTTP

### **Fase 4: LARGO PLAZO (1-3 Meses)**
- [ ] Migrar SQLite → PostgreSQL (producción)
- [ ] Implementar WAF (Web Application Firewall)
- [ ] Penetration testing
- [ ] Certificado SSL válido

---

## 5. CHECKLIST DE SEGURIDAD

```
AUTH & SESSION
  ☐ HTTPS obligatorio en producción
  ☐ JWT con expiración corta (15 min)
  ☐ Refresh tokens implementados
  ☐ HTTP-only, Secure, SameSite flags en cookies
  ☐ Validación de rol en endpoints sensibles

DATA PROTECTION
  ☐ Passwords con bcrypt/argon2 (nunca plaintext)
  ☐ API keys en .env, nunca en código
  ☐ Encriptación en tránsito (HTTPS)
  ☐ Encriptación en reposo para datos sensibles

INPUT VALIDATION
  ☐ Pydantic models para todos los inputs
  ☐ Validación de tipo MIME en uploads
  ☐ Límite de tamaño de archivos (10MB max)
  ☐ Sanitización de errores (no exponer detalles internos)

RATE LIMITING & DoS
  ☐ Rate limiting en endpoints públicos
  ☐ Límite de intentos de login (5 max)
  ☐ Timeout en queries largas
  ☐ Cuota de storage por usuario

AUDIT & LOGGING
  ☐ Audit trail de todas las acciones críticas
  ☐ Logs centralizados (no en plaintext)
  ☐ Rotación de logs
  ☐ No registrar tokens/passwords en logs

FILE UPLOAD SECURITY
  ☐ Validar MIME type
  ☐ Escanear malware (VirusTotal API)
  ☐ Servir archivos con auth
  ☐ Renombrar archivos (evitar path traversal)
```

---

## 6. CÓDIGO DE EJEMPLO: Implementar Upload Seguro

```python
# api/services.py
from fastapi import UploadFile, File, HTTPException
from pathlib import Path
import mimetypes
import os
from uuid import uuid4

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/api/v1/services/{service_id}/complete")
async def complete_service(
    service_id: int,
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
):
    # 1. Validar que el servicio existe y pertenece al usuario
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service or service.recycler_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # 2. Validar archivos
    for file in files:
        # Tipo MIME
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Formato no permitido: {file.content_type}"
            )
        
        # Tamaño
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Archivo demasiado grande")
        
        # Guardar con nombre seguro
        original_name = file.filename
        ext = Path(original_name).suffix
        safe_name = f"{uuid4()}{ext}"
        file_path = Path("uploads/evidencias") / safe_name
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 3. Registrar en DB
        evidence = Evidence(
            service_id=service_id,
            file_path=safe_name,  # NO la ruta completa
            uploaded_by=current_user.id
        )
        db.add(evidence)
    
    # 4. Actualizar estado del servicio
    service.status = "completado"
    service.completed_at = datetime.utcnow()
    db.commit()
    
    return {"status": "success", "evidence_count": len(files)}


# Servir archivos con autenticación
@router.get("/api/v1/evidence/{evidence_id}")
async def download_evidence(
    evidence_id: int,
    current_user: User = Depends(get_current_user),
):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404)
    
    # Validar acceso (propietario o admin)
    service = evidence.service
    if current_user.id not in [service.client_id, service.recycler_id] \
       and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    file_path = Path("uploads/evidencias") / evidence.file_path
    if not file_path.exists():
        raise HTTPException(status_code=404)
    
    return FileResponse(file_path, media_type="image/jpeg")
```

---

## 7. REFERENCIA: OWASP Top 10 (2021)

| Rango | Vulnerabilidad | Estado Reciclap | Acción |
|-------|----------------|-----------------|--------|
| A01 | Broken Access Control | ✗ Vulnerable | Implementar validación de rol |
| A02 | Cryptographic Failures | ✗ Vulnerable | Implementar HTTPS + encriptación |
| A03 | Injection | ✓ Mitigado (ORM) | Mantener |
| A04 | Insecure Design | ✗ Parcial | Threat modeling continuo |
| A05 | Security Misconfiguration | ✗ Vulnerable | Revisar config, env vars |
| A06 | Vulnerable Components | ? Desconocido | Hacer `pip audit` |
| A07 | Identification Failures | ✗ Vulnerable | 2FA, rate limiting |
| A08 | Data Integrity Failures | ✗ Vulnerable | Audit trail, validación |
| A09 | Logging Failures | ✗ Vulnerable | Implementar logs |
| A10 | SSRF | ✓ No aplica | N/A |

---

## 8. CONCLUSIÓN

**Reciclap tiene un nivel de riesgo ALTO** debido a múltiples vulnerabilidades en autenticación, encriptación y validación de acceso.

**Las acciones inmediatas recomendadas son:**

1. **🔴 CRÍTICA:** Rotar API keys y mover a .env
2. **🔴 CRÍTICA:** Implementar HTTPS en producción
3. **🔴 CRÍTICA:** Validación de rol en endpoints sensibles
4. **🟠 ALTA:** Rate limiting
5. **🟠 ALTA:** Audit trail

Con estas mitigaciones, el riesgo se reduce a **MEDIO**.

---

**Documento preparado por:** Claude (Security Analysis)  
**Metodología:** STRIDE Framework  
**Fecha:** 2026-05-04  
**Revisión siguiente:** 2026-05-18
