#!/usr/bin/env python3
"""
Script para gerar um arquivo TXT com a estrutura completa de diretórios e arquivos do projeto.
"""

import os
from pathlib import Path
from datetime import datetime


def generate_project_structure(output_file: str = "project_structure.txt"):
    """
    Gera um arquivo TXT com a estrutura completa do projeto.
    
    Args:
        output_file: Nome do arquivo de saída
    """
    project_root = Path(__file__).parent
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', '.idea', '.vscode'}
    ignore_files = {'.DS_Store', 'Thumbs.db'}
    
    structure = []
    structure.append("=" * 60)
    structure.append(f"ESTRUTURA DO PROJETO: {project_root.name}")
    structure.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    structure.append("=" * 60)
    structure.append("")
    
    for root, dirs, files in os.walk(project_root):
        # Filtrar diretórios ignorados
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        level = root.replace(str(project_root), '').count(os.sep)
        indent = ' ' * 2 * level
        rel_path = os.path.relpath(root, project_root)
        
        if rel_path == '.':
            structure.append(f"{project_root.name}/")
        else:
            structure.append(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        
        for file in files:
            if file not in ignore_files and not file.startswith('.'):
                file_ext = Path(file).suffix
                file_size = os.path.getsize(os.path.join(root, file))
                structure.append(f"{subindent}{file} ({file_size} bytes){file_ext}")
    
    # Salvar no arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(structure))
    
    print(f"✅ Estrutura salva em: {output_file}")
    print(f"📁 Total de diretórios: {sum(1 for _ in project_root.rglob('*') if _.is_dir())}")
    print(f"📄 Total de arquivos: {sum(1 for _ in project_root.rglob('*') if _.is_file())}")


def generate_detailed_structure(output_file: str = "detailed_structure.txt"):
    """
    Gera uma estrutura detalhada com informações adicionais.
    """
    project_root = Path(__file__).parent
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', '.idea', '.vscode'}
    
    structure = []
    structure.append("=" * 70)
    structure.append(f"ESTRUTURA DETALHADA DO PROJETO: {project_root.name}")
    structure.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    structure.append("=" * 70)
    structure.append("")
    
    python_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk(project_root):
        # Filtrar diretórios ignorados
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        level = root.replace(str(project_root), '').count(os.sep)
        indent = ' ' * 2 * level
        rel_path = os.path.relpath(root, project_root)
        
        if rel_path == '.':
            structure.append(f"📁 {project_root.name}/")
        else:
            structure.append(f"{indent}📁 {os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        
        for file in sorted(files):
            if file.startswith('.'):
                continue
                
            filepath = os.path.join(root, file)
            file_size = os.path.getsize(filepath)
            file_ext = Path(file).suffix
            
            # Contar linhas de código para arquivos Python
            line_count = 0
            if file.endswith('.py'):
                python_files += 1
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for line in f if line.strip())
                    total_lines += line_count
                except:
                    line_count = 0
            
            icon = "🐍" if file.endswith('.py') else "📄"
            size_info = f"{file_size:6d} bytes"
            lines_info = f" | {line_count:4d} linhas" if line_count > 0 else ""
            
            structure.append(f"{subindent}{icon} {file} ({size_info}{lines_info})")
    
    structure.append("")
    structure.append("=" * 70)
    structure.append(f"ESTATÍSTICAS:")
    structure.append(f"• Arquivos Python: {python_files}")
    structure.append(f"• Total de linhas de código: {total_lines}")
    structure.append(f"• Diretórios: {sum(1 for _ in project_root.rglob('*') if _.is_dir())}")
    structure.append(f"• Arquivos: {sum(1 for _ in project_root.rglob('*') if _.is_file())}")
    structure.append("=" * 70)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(structure))
    
    print(f"✅ Estrutura detalhada salva em: {output_file}")


if __name__ == "__main__":
    print("📋 Gerando estrutura do projeto...")
    generate_project_structure()
    print()
    generate_detailed_structure()
    print()
    print("🎉 Concluído! Verifique os arquivos:")
    print("   • project_structure.txt - Visão geral")
    print("   • detailed_structure.txt - Visão detalhada com estatísticas")