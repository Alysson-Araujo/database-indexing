# 📦 Guia de Versionamento - O que vai para o GitHub?

## 🎯 Resumo Rápido

### ✅ VAI PARA O GITHUB (Commit & Push)

```
✅ Código-fonte
✅ Configurações
✅ Documentação
✅ Scripts
✅ Migrations de banco
✅ Estrutura de pastas
✅ README e guias
```

### ❌ FICA NA SUA MÁQUINA (Ignorado pelo Git)

```
❌ Arquivos compilados (target/)
❌ Resultados de testes (results/*.json)
❌ Logs
❌ Arquivos temporários
❌ Configurações da IDE (.idea, .vscode)
❌ Dados sensíveis (.env, senhas)
❌ Cache do Python (__pycache__)
```

---

## 📂 Estrutura Detalhada

### ✅ CÓDIGO-FONTE (VAI)

```
src/
├── main/
│   ├── java/                           ✅ TODO o código Java
│   │   └── com/alysson/databaseindexing/
│   │       ├── controller/             ✅ Controllers
│   │       ├── service/                ✅ Services
│   │       ├── repository/             ✅ Repositories
│   │       ├── model/                  ✅ Models/Entities
│   │       └── DatabaseIndexingApplication.java ✅
│   │
│   └── resources/
│       ├── application.yml             ✅ Config padrão (SEM senhas!)
│       ├── application.properties      ✅ Config padrão
│       └── db/migration/               ✅ TODAS as migrations SQL
│           ├── V1__create_tables.sql   ✅
│           ├── V2__seed_data.sql       ✅
│           ├── V3__create_simple_indexes.sql ✅
│           ├── V4__create_composite_indexes.sql ✅
│           └── V5__create_covering_indexes.sql ✅
│
└── test/
    └── java/                           ✅ Testes unitários
```

**Por quê?** Esse é o coração do projeto. Outros devs precisam desse código.

---

### ✅ CONFIGURAÇÃO & INFRAESTRUTURA (VAI)

```
📄 pom.xml                              ✅ Dependências Maven
📄 docker-compose.yml                   ✅ Setup do PostgreSQL
📄 Dockerfile                           ✅ Containerização
📄 .gitignore                           ✅ Regras do Git
📄 .gitattributes                       ✅ Atributos do Git
📄 mvnw                                 ✅ Maven wrapper (Linux/Mac)
📄 mvnw.cmd                             ✅ Maven wrapper (Windows)
📁 .mvn/                                ✅ Config do Maven wrapper
```

**Por quê?** Permite que outros devs rodem o projeto sem instalar nada.

---

### ✅ SCRIPTS & FERRAMENTAS (VAI)

```
scripts/
├── analyze_results.py                  ✅ Script de análise
├── compare_all_tests.py                ✅ Comparação de testes
└── generate_html_report.py             ✅ Geração de relatórios

k6/scripts/
├── test-no-index.js                    ✅ Teste de carga
├── test-simple-index.js                ✅ Teste de carga
├── test-composite-index.js             ✅ Teste de carga
└── test-covering-index.js              ✅ Teste de carga

database/scripts/
└── generate_seed_data.py               ✅ Gerador de dados

📄 start-local.ps1                      ✅ Script de inicialização
📄 start.ps1                            ✅ Script de inicialização
```

**Por quê?** Outros devs precisam desses scripts para rodar testes.

---

### ✅ DOCUMENTAÇÃO (VAI)

```
docs/
├── README_COMPLETO.md                  ✅ Documentação técnica
├── POST_LINKEDIN.md                    ✅ Posts para LinkedIn
├── ARTIGO_LINKEDIN_COMPLETO.md         ✅ Artigo técnico
├── RELATORIO_BENCHMARK_FINAL.html      ✅ Relatório visual
├── COMPARATIVO_INDICES.txt             ✅ Comparação de resultados
├── RESUMO_EXECUTIVO.md                 ✅ Resumo do projeto
├── PROXIMOS_PASSOS.md                  ✅ Roadmap
└── O_QUE_FAZER_AGORA.md                ✅ Guia

📄 README.md                            ✅ README principal
📄 README_COMPLETO.md                   ✅ Guia completo
```

**Por quê?** Documentação é essencial para outros entenderem o projeto.

---

### ✅ ESTRUTURA DE PASTAS VAZIAS (VAI)

```
results/
└── .gitkeep                            ✅ Mantém pasta no Git

logs/
└── .gitkeep                            ✅ (se criar)
```

**Por quê?** `.gitkeep` é um arquivo vazio que força o Git a incluir pastas vazias.

---

## ❌ ARQUIVOS GERADOS (NÃO VAI)

### ❌ BUILD & COMPILAÇÃO

```
target/                                 ❌ TODO conteúdo
├── classes/                            ❌ .class compilados
├── DatabaseIndexing-0.0.1-SNAPSHOT.jar ❌ JAR gerado
├── test-classes/                       ❌ Testes compilados
└── maven-*/                            ❌ Cache do Maven
```

**Por quê?** Gerado automaticamente pelo `mvn clean install`. Ocupa espaço.

---

### ❌ RESULTADOS DE TESTES

```
results/
├── no-index.json                       ❌ Resultado k6 (~50MB)
├── simple-index.json                   ❌ Resultado k6
├── composite-index.json                ❌ Resultado k6
├── covering-index.json                 ❌ Resultado k6
├── *-summary.json                      ❌ Resumos
└── .gitkeep                            ✅ APENAS isso vai!
```

**Por quê?** Arquivos JSON de teste são **ENORMES** (50-100MB cada). Cada dev gera os seus próprios.

---

### ❌ CONFIGURAÇÕES DE IDE

```
.idea/                                  ❌ IntelliJ IDEA
├── workspace.xml                       ❌ Config pessoal
├── modules.xml                         ❌ Módulos
└── *.iml                               ❌ Arquivos de projeto

.vscode/                                ❌ VS Code
├── settings.json                       ❌ Config pessoal
└── launch.json                         ❌ Debug config

.settings/                              ❌ Eclipse
.project                                ❌ Eclipse
.classpath                              ❌ Eclipse
```

**Por quê?** Cada dev usa IDE diferente. Config pessoal não deve ser compartilhada.

---

### ❌ LOGS & TEMPORÁRIOS

```
logs/
├── application.log                     ❌ Logs de execução
└── error.log                           ❌ Logs de erro

*.log                                   ❌ Qualquer arquivo .log
*.tmp                                   ❌ Temporários
*.temp                                  ❌ Temporários
*.swp                                   ❌ Swap do Vim
```

**Por quê?** Logs são específicos de cada execução. Não agregam valor no Git.

---

### ❌ PYTHON CACHE

```
__pycache__/                            ❌ Cache do Python
├── analyze_results.cpython-*.pyc       ❌
└── *.pyc                               ❌

venv/                                   ❌ Ambiente virtual Python
env/                                    ❌ Ambiente virtual
```

**Por quê?** Cache é gerado automaticamente. Cada dev cria seu próprio venv.

---

### ❌ DADOS SENSÍVEIS

```
.env                                    ❌ Variáveis de ambiente
.env.local                              ❌ Config local
application-local.yml                   ❌ Config local com senhas
secrets/                                ❌ Pasta de segredos
*.pem                                   ❌ Certificados
*.key                                   ❌ Chaves privadas
```

**Por quê?** **NUNCA** commitar senhas, tokens, chaves privadas!

---

### ❌ ARQUIVOS DO SISTEMA OPERACIONAL

```
# Windows
Thumbs.db                               ❌ Cache de thumbnails
Desktop.ini                             ❌ Config de pasta
$RECYCLE.BIN/                           ❌ Lixeira

# MacOS
.DS_Store                               ❌ Metadata do Finder
._*                                     ❌ Resource forks

# Linux
*~                                      ❌ Backups automáticos
.directory                              ❌ KDE metadata
```

**Por quê?** Específicos do OS. Não têm utilidade no projeto.

---

## 🚀 Como Usar

### 1️⃣ Verificar o que vai ser commitado

```bash
git status
```

**Deve mostrar:**
- ✅ Arquivos de código (.java, .sql)
- ✅ Documentação (.md, .html)
- ✅ Scripts (.py, .js, .ps1)
- ✅ Configuração (pom.xml, docker-compose.yml)

**NÃO deve mostrar:**
- ❌ target/
- ❌ results/*.json
- ❌ .idea/
- ❌ *.log

### 2️⃣ Adicionar arquivos

```bash
# Adicionar tudo (gitignore já filtra)
git add .

# Ou específico
git add src/
git add docs/
git add scripts/
```

### 3️⃣ Commit

```bash
git commit -m "feat: Add database indexing benchmark project"
```

### 4️⃣ Push para GitHub

```bash
git push origin main
```

---

## 🔍 Verificar Tamanho do Repositório

### Antes de commitar:

```bash
# Ver tamanho do que será commitado
git ls-files -z | xargs -0 du -ch | tail -1
```

**Esperado:** < 5MB (sem results/*.json)

### Se ficou grande:

```bash
# Ver arquivos maiores
git ls-files | xargs ls -lh | sort -k5 -h -r | head -20
```

Se aparecer `results/*.json` ou `target/`:
```bash
git rm --cached results/*.json
git rm --cached -r target/
```

---

## 📊 Resumo Visual

```
┌─────────────────────────────────────────────────────────┐
│                    SEU PROJETO                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ✅ GITHUB                  ❌ SUA MÁQUINA              │
│  ┌──────────────┐          ┌──────────────┐            │
│  │ src/         │          │ target/      │            │
│  │ docs/        │          │ results/*.json│           │
│  │ scripts/     │          │ .idea/       │            │
│  │ k6/          │          │ logs/        │            │
│  │ pom.xml      │          │ .env         │            │
│  │ README.md    │          │ __pycache__/ │            │
│  │ .gitignore   │          │ *.log        │            │
│  │ docker-*.yml │          │ venv/        │            │
│  └──────────────┘          └──────────────┘            │
│                                                         │
│  🔄 Compartilhado          💻 Local                     │
│  📦 ~3-5 MB                💾 ~500 MB                   │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ IMPORTANTE: Dados Sensíveis

### ❌ NUNCA commite:

- Senhas de banco de dados
- Tokens de API
- Chaves privadas (.pem, .key)
- Dados pessoais de usuários
- Variáveis de ambiente (.env)

### ✅ Em vez disso:

**application.yml (GitHub):**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/benchmark_db
    username: ${DB_USERNAME:postgres}  # ← Variável de ambiente
    password: ${DB_PASSWORD:postgres}  # ← Variável de ambiente
```

**application-local.yml (NÃO commitado):**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/benchmark_db
    username: meu_user_real
    password: minha_senha_real_123
```

Adicione ao `.gitignore`:
```
application-local.yml
```

---

## 🎯 Checklist Final

Antes de fazer `git push`:

- [ ] `.gitignore` está atualizado
- [ ] `git status` não mostra `target/`
- [ ] `git status` não mostra `results/*.json`
- [ ] `git status` não mostra `.idea/` ou `.vscode/`
- [ ] Nenhum arquivo `.log` está sendo commitado
- [ ] Nenhuma senha está em arquivos de config
- [ ] README.md está completo
- [ ] Documentação está atualizada
- [ ] Tamanho do repo < 10MB

---

## 📚 Exemplo de Estrutura Final no GitHub

```
seu-usuario/database-indexing-benchmark/
├── 📁 .github/                        (workflows CI/CD - opcional)
├── 📁 .mvn/
├── 📁 database/
│   ├── migrations/
│   └── scripts/
├── 📁 docs/
│   ├── README_COMPLETO.md
│   ├── RELATORIO_BENCHMARK_FINAL.html
│   └── ...
├── 📁 k6/scripts/
├── 📁 results/
│   └── .gitkeep                       (APENAS isso!)
├── 📁 scripts/
├── 📁 src/
│   ├── main/
│   └── test/
├── 📄 .gitattributes
├── 📄 .gitignore
├── 📄 docker-compose.yml
├── 📄 Dockerfile
├── 📄 mvnw
├── 📄 mvnw.cmd
├── 📄 pom.xml
├── 📄 README.md
├── 📄 README_COMPLETO.md
└── 📄 start-local.ps1
```

**Tamanho esperado:** 3-5 MB

---

## 🆘 Troubleshooting

### Problema: "git push" muito lento

**Causa:** Provavelmente está tentando subir `results/*.json` ou `target/`

**Solução:**
```bash
# Ver o que está sendo enviado
git ls-files --cached | grep -E "(results|target)"

# Remover do cache (não deleta do disco)
git rm --cached results/*.json
git rm --cached -r target/

# Commitar a remoção
git commit -m "chore: Remove generated files from git"
```

---

### Problema: Arquivo sensível foi commitado

**Se ainda não fez push:**
```bash
git reset HEAD~1  # Desfaz último commit
# Edita .gitignore
git add .gitignore
git commit -m "chore: Update gitignore"
```

**Se já fez push (CRÍTICO!):**
```bash
# Remover do histórico (perigoso!)
git filter-branch --tree-filter 'rm -f .env' HEAD
git push --force
```

⚠️ **Melhor:** Trocar a senha/token que vazou imediatamente!

---

## ✅ Conclusão

**VAI PARA GITHUB:**
- ✅ Todo código-fonte
- ✅ Configurações (sem senhas!)
- ✅ Documentação
- ✅ Scripts
- ✅ Estrutura de pastas

**FICA NA MÁQUINA:**
- ❌ Arquivos compilados
- ❌ Resultados de testes
- ❌ Configurações de IDE
- ❌ Logs
- ❌ Dados sensíveis
- ❌ Cache

**Lembre-se:** O `.gitignore` já está configurado para filtrar tudo automaticamente! 🎉

