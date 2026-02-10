import json
import statistics
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir) if script_dir.endswith('scripts') else script_dir

print("\n" + "="*50)
print("   ANÁLISE RESULTADOS K6 - TESTE SIMPLES")
print("="*50 + "\n")

file_path = os.path.join(base_dir, "results/simple-index.json")

try:
    durations = []
    status_200 = 0
    status_404 = 0
    status_500 = 0
    other_status = 0
    iterations = 0
    vus_max = 0
    line_count = 0

    print(f"Processando arquivo: {file_path}")
    print("Aguarde...\n")

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1

            if line_count % 10000 == 0:
                print(".", end="", flush=True)

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
                            else:
                                other_status += 1


                    elif metric == 'iterations':
                        iterations += 1


                    elif metric == 'vus':
                        value = data.get('data', {}).get('value')
                        if value:
                            vus_max = max(vus_max, int(value))

            except json.JSONDecodeError:
                continue
            except Exception:
                continue

    print("\n")
    print("="*50)
    print("   RESULTADOS")
    print("="*50 + "\n")


    if durations:
        durations_sorted = sorted(durations)
        count = len(durations_sorted)

        min_val = durations_sorted[0]
        max_val = durations_sorted[-1]
        avg_val = statistics.mean(durations_sorted)

        p50 = durations_sorted[int(count * 0.50)]
        p90 = durations_sorted[int(count * 0.90)]
        p95 = durations_sorted[int(count * 0.95)]
        p99 = durations_sorted[int(count * 0.99)]

        print("LATÊNCIA HTTP:")
        print(f"  Mínima:          {min_val:.2f} ms")
        print(f"  Média:           {avg_val:.2f} ms")
        print(f"  P50 (mediana):   {p50:.2f} ms")
        print(f"  P90:             {p90:.2f} ms")
        print(f"  P95:             {p95:.2f} ms {'✓' if p95 < 300 else '✗'}")
        print(f"  P99:             {p99:.2f} ms {'✓' if p99 < 500 else '✗'}")
        print(f"  Máxima:          {max_val:.2f} ms")
        print()


    total_reqs = status_200 + status_404 + status_500 + other_status
    if total_reqs > 0:
        print("REQUISIÇÕES HTTP:")
        print(f"  Total:           {total_reqs} requisições")
        print(f"  200 (OK):        {status_200} ({(status_200/total_reqs)*100:.1f}%)")
        print(f"  404 (Not Found): {status_404} ({(status_404/total_reqs)*100:.1f}%)")

        if status_500 > 0:
            print(f"  500 (Server Error): {status_500} ({(status_500/total_reqs)*100:.1f}%)")

        if other_status > 0:
            print(f"  Outros:          {other_status} ({(other_status/total_reqs)*100:.1f}%)")

        error_rate = ((status_404 + status_500 + other_status) / total_reqs) * 100
        print(f"\n  Taxa de Erro:    {error_rate:.2f}% {'✓' if error_rate < 10 else '✗'}")
        print()


    print("CARGA DE TESTE:")
    print(f"  Iterações:       {iterations}")
    print(f"  VUs Máximo:      {vus_max} usuários virtuais")
    print(f"  Linhas processadas: {line_count}")
    print()


    if total_reqs > 0:
        duration_seconds = 240  # 4 minutos
        reqs_per_sec = total_reqs / duration_seconds
        print("THROUGHPUT:")
        print(f"  Req/seg:         {reqs_per_sec:.2f} requisições/segundo")
        print()


    print("="*50)
    print("   DIAGNÓSTICO")
    print("="*50 + "\n")

    if durations and p95 < 300:
        print("✓ [OK] P95 < 300ms - Latência dentro do esperado!")
    elif durations:
        print("✗ [ALERTA] P95 >= 300ms - Latência acima do esperado!")

    if error_rate < 10:
        print("✓ [OK] Taxa de erro < 10% - Dentro do threshold!")
    else:
        print("✗ [FALHA] Taxa de erro >= 10% - Threshold ultrapassado!")
        print("          Motivo: Muitas requisições 404/500")

    if status_404 > 0:
        print("\nℹ [INFO] Erros 404 são esperados quando o teste busca")
        print("         IDs/emails aleatórios que podem não existir.")

    print("\n" + "="*50)
    print("   ANÁLISE CONCLUÍDA!")
    print("="*50 + "\n")

except FileNotFoundError:
    print(f"ERRO: Arquivo não encontrado: {file_path}")
    sys.exit(1)
except Exception as e:
    print(f"ERRO: {e}")
    sys.exit(1)
