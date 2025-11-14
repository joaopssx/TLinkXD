# TLinkXD

App em Python para conectar um PC Windows a um Termux via WiFi, exibindo status do sistema do PC no Termux, incluindo monitoramento avançado de disco (IO, partições), temperatura (CPU, sistema), rede, processos, bateria, com UI colorida e gráficos ASCII.

## Funcionalidades Implementadas
- Detecta automaticamente plataforma (Windows servidor, Termux cliente).
- Coleta e envia stats via JSON filtrado.
- UI colorida com colorama para ambas plataformas.
- Gráficos de barra ASCII com # (10 # = 100%, cada # = 10%) para percentuais como CPU, RAM, bateria.
- Monitoramento de disco: IO speeds, partições.
- Monitoramento de temperatura: CPU e sensores adicionais.
- Alertas para thresholds altos (ex.: CPU > 80%).
- Logging de stats e eventos.
- Display local no servidor Windows.
- Configurações expandidas com mais JSONs.
- Licença: MIT.

## 10+ Ideias Diferentes para o App (Expansões Futuras ou Inventadas)
1. **Monitoramento de GPU**: Adicionar stats de uso e temp de GPU usando libs como GPUtil.
2. **Velocidade de Fans**: Monitorar RPM de fans via psutil ou WMI.
3. **Logging Avançado**: Exportar logs para CSV/JSON para análise histórica.
4. **Alertas por Email/SMS**: Enviar notificações via SMTP ou API se thresholds excedidos.
5. **Comandos Remotos**: Permitir que Termux envie comandos como shutdown ou kill process para o PC.
6. **Transferência de Arquivos**: Função para enviar/receber files entre PC e Termux.
7. **Captura de Tela**: Enviar screenshots do PC para visualização no Termux.
8. **Gerenciamento de Processos**: Listar e gerenciar (kill/start) processos remotamente.
9. **Verificação de Atualizações**: Checar updates do sistema e apps no PC.
10. **Suporte Multi-Cliente**: Permitir múltiplos Termux conectados ao mesmo servidor.
11. **Encriptação de Dados**: Usar SSL/TLS para conexões seguras.
12. **Temas Customizáveis**: Mais opções de cores e layouts via config.
13. **Integração com IoT**: Monitorar dispositivos conectados via rede.
14. **Gráficos Avançados**: Evoluir ASCII para plots com matplotlib (exportar imagens).
15. **Modo Offline**: Cache de stats para visualização sem conexão.

## Instalação
1. Instale Python 3.x.
2. No Windows: `pip install psutil pywin32 colorama`.
3. No Termux: `pkg install python`, `pip install psutil colorama`.
4. Rode `python src/main.py`.

## Uso
- Windows: Inicia servidor, mostra stats locais coloridos.
- Termux: Conecta e exibe com cores e barras.

Repo: https://github.com/joaopssx/TLinkXD
