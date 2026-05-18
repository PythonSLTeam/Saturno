# -*- coding: utf-8 -*-
"""
Saturno Language Engine
Desenvolvido por: PythonSLTeam
Equipe oficial do projeto Saturno.
"""

import re
import sys

class SaturnoRuntimeError(Exception):
    """Classe para capturar erros em tempo de execução no Saturno"""
    pass

class SaturnoEngine:
    def __init__(self):
        # Escopo global da linguagem (onde ficam salvas as variáveis)
        self.variaveis = {}
        # Histórico de saída para quando a linguagem for usada em modo embutido
        self.historico_saida = []

    def limpar_memoria(self):
        """Limpa as variáveis e o histórico do motor de Saturno"""
        self.variaveis.clear()
        self.historico_saida.clear()

    def _avaliar_expressao(self, expressao, linha_num):
        """Avalia expressões matemáticas ou lógicas com segurança no contexto de Saturno"""
        # Remove espaços desnecessários
        expressao = expressao.strip()
        
        # Se for uma string pura entre aspas
        if (expressao.startswith('"') and expressao.endswith('"')) or (expressao.startswith("'") and expressao.endswith("'")):
            return expressao[1:-1]
            
        try:
            # Executa a expressão usando o dicionário de variáveis do Saturno como escopo seguro
            return eval(expressao, {"__builtins__": None}, self.variaveis)
        except NameError as ne:
            raise SaturnoRuntimeError(f"[Linha {linha_num}] Erro de Nome: A variável ou comando {ne} não foi definido em Saturno.")
        except SyntaxError:
            raise SaturnoRuntimeError(f"[Linha {linha_num}] Erro de Sintaxe: A expressão '{expressao}' é inválida.")
        except Exception as e:
            raise SaturnoRuntimeError(f"[Linha {linha_num}] Erro ao processar expressão '{expressao}': {e}")

    def executar(self, codigo_fonte, capturar_saida=False):
        """
        Executa uma string contendo código Saturno.
        Se 'capturar_saida' for True, ele retorna uma lista com o que foi orbitado
        em vez de printar direto no terminal.
        """
        self.historico_saida = []
        linhas = codigo_fonte.split('\n')
        
        for i, linha in enumerate(linhas, start=1):
            linha = linha.strip()
            
            # Ignora linhas vazias ou comentários espaciais '#'
            if not linha or linha.startswith('#'):
                continue

            try:
                # 1. Comando: orbitar (Equivalente ao print)
                if linha.startswith('orbitar '):
                    conteudo = linha[8:].strip()
                    resultado = self._avaliar_expressao(conteudo, i)
                    
                    if capturar_saida:
                        self.historico_saida.append(str(resultado))
                    else:
                        print(resultado)

                # 2. Comando: definir (Criação de variáveis)
                elif linha.startswith('definir '):
                    match = re.match(r'definir\s+(\w+)\s*=\s*(.*)', linha)
                    if match:
                        nome_var = match.group(1)
                        expressao = match.group(2).strip()
                        
                        # Calcula o valor e salva no dicionário de variáveis
                        self.variaveis[nome_var] = self._avaliar_expressao(expressao, i)
                    else:
                        raise SaturnoRuntimeError(f"[Linha {i}] Erro de Sintaxe: Uso incorreto do comando 'definir'. Use: definir variavel = valor")

                # 3. Comando desconhecido
                else:
                    # Verifica se o usuário tentou fazer uma atribuição direta sem o 'definir'
                    if '=' in linha and not linha.startswith('definir '):
                        raise SaturnoRuntimeError(f"[Linha {i}] Comando Desconhecido: Em Saturno, você precisa usar a palavra-chave 'definir' para criar variáveis.")
                    else:
                        raise SaturnoRuntimeError(f"[Linha {i}] Comando Desconhecido: Não reconheço a órbita de comando: '{linha}'")
            
            except SaturnoRuntimeError as e:
                print(f"Erro em Saturno: {e}", file=sys.stderr)
                if capturar_saida:
                    return [f"Erro: {e}"]
                return False

        if capturar_saida:
            return self.historico_saida
        return True

# Função auxiliar de atalho para facilitar o uso da biblioteca pela comunidade
def rodar(codigo):
    """Atalho rápido para executar códigos Saturno instantaneamente"""
    engine = SaturnoEngine()
    return engine.executar(codigo)
