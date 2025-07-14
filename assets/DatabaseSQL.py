import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="SolidDatabase.db"):
        self.db_name = db_name
        self.create_database()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_database(self):
        self.connect()
        
        # Criar tabela de programas com apenas id, nome e caminhoArquivo
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS programas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            caminhoArquivo TEXT NOT NULL
        )
        ''')
        
        self.conn.commit()
        self.disconnect()

    def adicionar_programa(self, nome, caminhoArquivo):
        """Adiciona um novo programa ao banco de dados"""
        self.connect()
        try:
            self.cursor.execute('''
            INSERT INTO programas (nome, caminhoArquivo)
            VALUES (?, ?)
            ''', (nome, caminhoArquivo))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao adicionar programa: {e}")
            return False
        finally:
            self.disconnect()

    def buscar_programa(self, id=None):
        """Busca programas no banco de dados"""
        self.connect()
        try:
            if id:
                programa = self.cursor.execute('''
                SELECT * FROM programas 
                WHERE id = ?
                ''', (f'%{id}%',))
                self.cursor.fetchall()
                return programa

            else:
                self.cursor.execute('SELECT * FROM programas')
                return self.cursor.fetchall()
            
        finally:
            self.disconnect()

    def atualizar_programa(self, id, nome=None, caminhoArquivo=None):
        """Atualiza informações de um programa existente"""
        self.connect()
        try:
            update_fields = []
            values = []
            
            if nome:
                update_fields.append("nome = ?")
                values.append(nome)
            if caminhoArquivo:
                update_fields.append("caminhoArquivo = ?")
                values.append(caminhoArquivo)
            
            if update_fields:
                query = f'''
                UPDATE programas 
                SET {', '.join(update_fields)}
                WHERE id = ?
                '''
                values.append(id)
                
                self.cursor.execute(query, values)
                self.conn.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar programa: {e}")
            return False
        finally:
            self.disconnect()

    def remover_programa(self, id):
        """Remove um programa do banco de dados"""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM programas WHERE id = ?', (id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover programa: {e}")
            return False
        finally:
            self.disconnect()
    

