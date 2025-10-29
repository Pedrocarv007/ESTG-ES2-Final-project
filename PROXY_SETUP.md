# StudyHub AI - Configuração de Proxy Reverso

## Modos de Execução

Este projeto suporta dois modos de execução:

### 1. Modo Proxy Reverso (Recomendado para produção)
- URLs com prefixo `/studyhubai`
- Funciona com IIS e proxy reverso
- Exemplo: `http://localhost/studyhubai/auth/login`

### 2. Modo Direto (Desenvolvimento)
- URLs diretas sem prefixo
- Acesso direto à porta 6002
- Exemplo: `http://localhost:6002/auth/login`

## Como Configurar

### Usando PowerShell (Recomendado)
```powershell
# Para modo proxy reverso
.\configure.ps1 proxy

# Para modo direto
.\configure.ps1 direct
```

### Usando scripts batch
```cmd
# Para modo proxy reverso
start_proxy.bat

# Para modo direto
start_direct.bat
```
}

### Configuração Manual
1. Copie o arquivo de configuração desejado:
   - `.env.proxy` → `.env` (para modo proxy)
   - `.env.direct` → `.env` (para modo direto)

2. Execute a aplicação:
   ```
   python run.py
   ```

## Configuração do IIS

Seu `web.config` já está configurado corretamente:

```xml
<!-- StudyHubAI - endpoints de API -->
<rule name="StudyHubAIAPI" stopProcessing="true">
  <match url="^studyhubai/(auth|user|material)(.*)" />
  <action type="Rewrite" url="http://localhost:6002/{R:1}{R:2}" />
</rule>

<!-- StudyHubAI - restante (catch-all do microsserviço) -->
<rule name="StudyHubAI" stopProcessing="true">
  <match url="^studyhubai/(.*)" />
  <action type="Rewrite" url="http://localhost:6002/{R:1}" />
</rule>
```

## Como Funciona

### Modo Proxy (`USE_PROXY=true`)
- Flask registra blueprints com prefixo `/studyhubai`
- URLs geradas incluem automaticamente o prefixo
- Arquivos estáticos servidos com prefixo correto
- Funciona tanto via proxy quanto acesso direto

### Modo Direto (`USE_PROXY=false`)
- Flask registra blueprints sem prefixo
- URLs geradas são diretas
- Ideal para desenvolvimento local

## Testando

### Teste do Modo Proxy
1. Execute: `.\configure.ps1 proxy`
2. Inicie: `python run.py`
3. Acesse: `http://localhost:6002/studyhubai/`
4. Via proxy: `http://localhost/studyhubai/`

### Teste do Modo Direto
1. Execute: `.\configure.ps1 direct`
2. Inicie: `python run.py`
3. Acesse: `http://localhost:6002/`

## Variáveis de Ambiente

| Variável | Proxy | Direto | Descrição |
|----------|-------|--------|-----------|
| `USE_PROXY` | `true` | `false` | Ativa/desativa modo proxy |
| `APPLICATION_ROOT` | `/studyhubai` | `` | Prefixo da aplicação |
| `FLASK_PORT` | `6002` | `6002` | Porta do Flask |

## Endpoints de Health Check

- Modo Proxy: `/studyhubai/health` e `/health`
- Modo Direto: `/health`