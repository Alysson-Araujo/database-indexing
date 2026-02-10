import json
import statistics
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir) if script_dir.endswith('scripts') else script_dir

print("\n" + "="*70)
print("   ANÁLISE COMPARATIVA - IMPACTO DE ÍNDICES NO DESEMPENHO")
print("="*70 + "\n")

test_files = {
    'Sem Índices': os.path.join(base_dir, 'results/no-index.json'),
    'Índices Simples': os.path.join(base_dir, 'results/simple-index.json'),
    'Índices Compostos': os.path.join(base_dir, 'results/composite-index.json'),
    'Covering Indexes': os.path.join(base_dir, 'results/covering-index.json')
}

results = {}

def analyze_file(file_path):
    durations = []
    status_200 = 0
    status_404 = 0
    status_500 = 0
    iterations = 0
    vus_max = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())

                    if data.get('type') == 'Point':
                        metric = data.get('metric')

                        if metric == 'http_req_duration':
                            value = data.get('data', {}).get('value')
                            if value:
                                durations.append(float(value))

                                status = data.get('data', {}).get('tags', {}).get('status')
                                if status == '200':
                                    status_200 += 1
                                elif status == '404':
                                    status_404 += 1
                                elif status == '500':
                                    status_500 += 1

                        elif metric == 'iterations':
                            iterations += 1

                        elif metric == 'vus':
                            value = data.get('data', {}).get('value')
                            if value:
                                vus_max = max(vus_max, int(value))

                except:
                    continue

        if durations:
            durations_sorted = sorted(durations)
            count = len(durations_sorted)

            return {
                'min': durations_sorted[0],
                'max': durations_sorted[-1],
                'avg': statistics.mean(durations_sorted),
                'p50': durations_sorted[int(count * 0.50)],
                'p90': durations_sorted[int(count * 0.90)],
                'p95': durations_sorted[int(count * 0.95)],
                'p99': durations_sorted[int(count * 0.99)],
                'status_200': status_200,
                'status_404': status_404,
                'status_500': status_500,
                'total_reqs': status_200 + status_404 + status_500,
                'iterations': iterations,
                'vus_max': vus_max,
                'throughput': (status_200 + status_404 + status_500) / 240
            }
    except FileNotFoundError:
        return None

print("Analisando testes...")
for name, file_path in test_files.items():
    print(f"  - {name}...", end=" ")
    result = analyze_file(file_path)
    if result:
        results[name] = result
        print("✓")
    else:
        print("✗ (arquivo não encontrado)")

print("\n" + "="*70)
print("   COMPARATIVO DE LATÊNCIA (em milissegundos)")
print("="*70 + "\n")

print(f"{'Métrica':<20} {'Sem Índices':<15} {'Simples':<15} {'Compostos':<15} {'Covering':<15}")
print("-" * 80)

metrics = ['min', 'avg', 'p50', 'p90', 'p95', 'p99', 'max']
metric_names = {
    'min': 'Mínima',
    'avg': 'Média',
    'p50': 'P50 (Mediana)',
    'p90': 'P90',
    'p95': 'P95',
    'p99': 'P99',
    'max': 'Máxima'
}

for metric in metrics:
    values = []
    print(f"{metric_names[metric]:<20}", end="")

    for name in ['Sem Índices', 'Índices Simples', 'Índices Compostos', 'Covering Indexes']:
        if name in results and metric in results[name]:
            value = results[name][metric]
            values.append(value)
            print(f"{value:>12.2f} ms ", end="")
        else:
            print(f"{'N/A':>15}", end="")

    print()

print("\n" + "="*70)
print("   GANHO DE PERFORMANCE (vs Sem Índices)")
print("="*70 + "\n")

if 'Sem Índices' in results:
    baseline_p95 = results['Sem Índices']['p95']
    baseline_avg = results['Sem Índices']['avg']

    print(f"{'Tipo de Índice':<25} {'P95':<20} {'Melhoria P95':<20} {'Média':<15}")
    print("-" * 80)

    for name in ['Sem Índices', 'Índices Simples', 'Índices Compostos', 'Covering Indexes']:
        if name in results:
            p95 = results[name]['p95']
            avg = results[name]['avg']

            if name == 'Sem Índices':
                improvement = "Baseline"
                improvement_pct = "0%"
            else:
                improvement = baseline_p95 / p95 if p95 > 0 else 0
                improvement_pct = f"{((baseline_p95 - p95) / baseline_p95 * 100):.1f}% mais rápido"

            symbol = "✓" if p95 < 300 else "✗"
            print(f"{name:<25} {p95:>8.2f} ms {symbol:<9} {improvement_pct:<20} {avg:>8.2f} ms")

print("\n" + "="*70)
print("   THROUGHPUT & CAPACIDADE")
print("="*70 + "\n")

print(f"{'Tipo de Índice':<25} {'Req/seg':<15} {'Total Reqs':<15} {'Iterações':<15}")
print("-" * 80)

for name in ['Sem Índices', 'Índices Simples', 'Índices Compostos', 'Covering Indexes']:
    if name in results:
        throughput = results[name]['throughput']
        total_reqs = results[name]['total_reqs']
        iterations = results[name]['iterations']

        print(f"{name:<25} {throughput:>10.2f} {total_reqs:>15} {iterations:>15}")


print("\n" + "="*70)
print("   TAXA DE SUCESSO")
print("="*70 + "\n")

print(f"{'Tipo de Índice':<25} {'200 OK':<15} {'404':<15} {'500':<15} {'Taxa Sucesso':<15}")
print("-" * 80)

for name in ['Sem Índices', 'Índices Simples', 'Índices Compostos', 'Covering Indexes']:
    if name in results:
        s200 = results[name]['status_200']
        s404 = results[name]['status_404']
        s500 = results[name]['status_500']
        total = results[name]['total_reqs']

        success_rate = (s200 / total * 100) if total > 0 else 0

        print(f"{name:<25} {s200:>10} {s404:>15} {s500:>15} {success_rate:>12.1f}%")


print("\n" + "="*70)
print("   RESUMO & RECOMENDAÇÕES")
print("="*70 + "\n")

if len(results) >= 2:

    best_p95 = min(results.values(), key=lambda x: x['p95'])
    best_name = [k for k, v in results.items() if v['p95'] == best_p95['p95']][0]

    print(f"🏆 MELHOR PERFORMANCE: {best_name}")
    print(f"   P95: {best_p95['p95']:.2f} ms")
    print(f"   Média: {best_p95['avg']:.2f} ms")
    print(f"   Throughput: {best_p95['throughput']:.2f} req/s")

    print(f"\n📊 IMPACTO DOS ÍNDICES:")

    if 'Sem Índices' in results and best_name != 'Sem Índices':
        improvement = results['Sem Índices']['p95'] / best_p95['p95']
        print(f"   {best_name} é {improvement:.1f}x MAIS RÁPIDO que sem índices!")

    print(f"\n💡 RECOMENDAÇÕES:")
    print(f"   1. Use Covering Indexes para queries frequentes que retornam poucos campos")
    print(f"   2. Use Índices Compostos para queries com múltiplos filtros (WHERE)")
    print(f"   3. Índices Simples são suficientes para queries com filtro único")
    print(f"   4. Evite queries sem índices em produção (muito lentas!)")

    print(f"\n✅ CONCLUSÃO:")
    if 'Covering Indexes' in results and 'Sem Índices' in results:
        improvement = results['Sem Índices']['p95'] / results['Covering Indexes']['p95']
        pct = ((results['Sem Índices']['p95'] - results['Covering Indexes']['p95']) / results['Sem Índices']['p95'] * 100)
        print(f"   Índices melhoram a performance em até {improvement:.1f}x ({pct:.0f}% mais rápido)!")
        print(f"   O investimento em indexação é ESSENCIAL para performance!")

print("\n" + "="*70)
print("   ANÁLISE COMPARATIVA CONCLUÍDA!")
print("="*70 + "\n")


print("Salvando relatório em COMPARATIVO_INDICES.txt...")

output_file = os.path.join(base_dir, 'docs/COMPARATIVO_INDICES.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("   RELATÓRIO COMPARATIVO - IMPACTO DE ÍNDICES\n")
    f.write("="*70 + "\n\n")

    f.write(f"Testes executados: {len(results)}\n")
    f.write(f"Data: 2026-02-09\n\n")

    f.write("RESUMO P95 (Principal métrica de performance):\n")
    for name in ['Sem Índices', 'Índices Simples', 'Índices Compostos', 'Covering Indexes']:
        if name in results:
            f.write(f"  {name:<25} P95 = {results[name]['p95']:>8.2f} ms\n")

    f.write(f"\nMelhor performance: {best_name}\n")

    if 'Sem Índices' in results and best_name != 'Sem Índices':
        improvement = results['Sem Índices']['p95'] / best_p95['p95']
        f.write(f"Melhoria: {improvement:.1f}x mais rápido que sem índices\n")

print("✓ Relatório salvo!\n")


