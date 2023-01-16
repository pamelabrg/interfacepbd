from tkinter import *
from tkinter import ttk
import mysql.connector

root = Tk()

class Funcs():
    ##FUNÇÕES GERAIS BD
    def limpa_tela2(self):
        self.entry_nomeCliente.delete(0, END)
        self.entry_primeiroSobrenome.delete(0, END)
        self.entry_ultimoSobrenome.delete(0, END)
        self.entry_cpf.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_telefone.delete(0, END)
        self.entry_endereco.delete(0, END)
    def conexao_bd(self):
        self.conn =  mysql.connector.connect(host='localhost', user='root', password='123456', database='trabalho_final')
        self.cursor = self.conn.cursor();
    def desconectar_bd(self):
        self.conn.close();
    
    ##FUNCOES ABA PROJETOS        -1
    def limpa_tela1(self):
        self.entry_cod.delete(0, END)
        self.entry_pot.delete(0, END)
        self.entry_data.delete(0, END)
        self.entry_venda.delete(0, END)
        self.entry_uc.delete(0, END)
        self.entry_SN.delete(0, END)
        self.entry_codInversor.delete(0, END)
        self.entry_qtdInversor.delete(0, END)
        self.entry_codModulos.delete(0, END)
        self.entry_qtdModulos.delete(0, END)
        self.select_projetosLista()
    def variaveisProjeto(self):
        self.codigo = self.entry_cod.get()
        self.pot = self.entry_pot.get()
        self.data = self.entry_data.get()
        self.venda = self.entry_venda.get()
        self.concessionaria = self.Tipvar1.get()
        self.ligacao = self.Tipvar2.get()
        self.uc = self.entry_uc.get()
        self.engenheiro = self.Tipvar3.get()
        self.SN = self.entry_SN.get()
        self.codInversor = self.entry_codInversor.get()
        self.qtdInversor = self.entry_qtdInversor.get()
        self.codModulos = self.entry_codModulos.get()
        self.qtdModulos = self.entry_qtdModulos.get()
    def add_projeto(self):
        self.variaveisProjeto()
        self.conexao_bd()

        self.cursor.execute("""SELECT idConcessionaria FROM Concessionaria WHERE nome = '%s'""" % (self.concessionaria))
        id_concessionaria1 = self.cursor.fetchall()
        id_concessionaria= id_concessionaria1[0]
        
        self.cursor.execute("""SELECT crea FROM engenheiro WHERE pnomeEng = '%s'""" % (self.engenheiro))
        id_engenheiro1 = self.cursor.fetchall()
        id_engenheiro = id_engenheiro1[0]

        self.cursor.execute("""INSERT INTO projeto (idProjeto, potencia, dataInstalacao, idConcessionaria, tipoLigacao, ucGeradora, idVenda, crea)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (self.codigo, self.pot, self.data, id_concessionaria[0], self.ligacao, self.uc, self.venda, id_engenheiro[0]))
        self.cursor.execute("""INSERT INTO registromodulos VALUES (%s, %s, %s);""", (self.codigo, self.codModulos, self.qtdModulos))
        self.cursor.execute("""INSERT INTO registroinversor VALUES (%s, %s, %s, %s);""", (self.SN, self.codigo, self.codInversor, self.qtdInversor))
        self.conn.commit()
        self.desconectar_bd()
        self.select_projetosLista()
        self.limpa_tela1()
    def select_projetosLista(self):
        self.listaProjetos.delete(*self.listaProjetos.get_children())
        self.conexao_bd()
        sql = "SELECT idProjeto, potencia, dataInstalacao, idConcessionaria, tipoLigacao, ucGeradora, idVenda, crea FROM projeto  ORDER BY idProjeto"
        self.cursor.execute(sql)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaProjetos.insert("", "end", values=i)
        self.desconectar_bd()
    def doubleClickProjetos(self, event):
        self.conexao_bd()
        self.limpa_tela1()
        self.variaveisProjeto()
        self.listaProjetos.selection()

        for n in self.listaProjetos.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.listaProjetos.item(n, "values")
            self.entry_cod.insert(END, col1)
            self.entry_pot.insert(END, col2)
            self.entry_data.insert(END, col3)
            self.cursor.execute("SELECT nome FROM Concessionaria WHERE idConcessionaria = '%s'" % col4)
            conc = self.cursor.fetchall()
            self.Tipvar1.set(conc[0])
            self.Tipvar2.set(col5)
            self.entry_uc.insert(END, col6)
            self.entry_venda.insert(END, col7)
            self.cursor.execute("SELECT pnomeEng FROM engenheiro WHERE crea = '%s'" % col8)
            crea = self.cursor.fetchall()
            self.Tipvar3.set(crea[0])
    def deleta_projeto(self):
        self.codigo = self.entry_cod.get()
        self.conexao_bd()
        self.cursor.execute("""DELETE FROM projeto WHERE idProjeto = %s""" % (self.codigo))
        self.conn.commit()
        self.desconectar_bd()
        self.select_projetosLista()
        self.limpa_tela1()
    def altera_projeto(self):
        self.variaveisProjeto()
        self.conexao_bd()
        self.cursor.execute("""UPDATE projeto SET potencia = %s, dataInstalacao = %s, idVenda = %s, ucGeradora = %s WHERE idProjeto = %s""", 
            (self.pot, self.data, self.venda, self.uc, self.codigo)); 
        self.conn.commit()
        self.desconectar_bd()
        self.select_projetosLista()
        self.limpa_tela1()
    def busca_projeto(self):
        self.conexao_bd()
        self.variaveisProjeto()
        self.listaProjetos.delete(*self.listaProjetos.get_children())
        self.entry_cod.insert(END, '%')
        codigo = self.entry_cod.get()
        self.cursor.execute(""" SELECT idProjeto, potencia, dataInstalacao, idConcessionaria, tipoLigacao, ucGeradora, idVenda, crea FROM projeto WHERE idProjeto LIKE '%s' ORDER BY idProjeto""" % (codigo))
        busca = self.cursor.fetchall()
        for i in busca:
            self.listaProjetos.insert("", "end", values=i)
        self.desconectar_bd()
        self.limpa_tela1()
    
    ##FUNÇÕES ABA vendas        -2
    def limpa_tela2(self):
        self.entry_idVenda.delete(0, END)
        self.entry_valor.delete(0, END)
        self.entry_dataVenda.delete(0, END)
        self.entry_vendedorVenda.delete(0, END)
        self.entry_cliente.delete(0, END)
        self.select_vendasLista()
    def variaveisVendas(self):
        self.idVenda = self.entry_idVenda.get()
        self.valor = self.entry_valor.get()
        self.dataVenda = self.entry_dataVenda.get()
        self.vendedorVenda = self.entry_vendedorVenda.get()
        self.clienteVenda = self.entry_cliente.get()
    def select_vendasLista(self):
        self.listaVendas.delete(*self.listaVendas.get_children())
        self.conexao_bd()
        sql2 = "SELECT idVenda, pnomeCliente, mnomeCliente, valor, dataVenda, pnomeVendedor FROM cliente INNER JOIN (SELECT idVenda, valor, dataVenda, pnomeVendedor, cpf FROM venda INNER JOIN vendedor ON venda.idVendedor = vendedor.idVendedor) AS test ON cliente.cpf = test.cpf ORDER by pnomeCliente"
        self.cursor.execute(sql2)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaVendas.insert("", "end", values=i)
        self.desconectar_bd()    
    def add_novaVenda(self):
        self.variaveisVendas()
        self.conexao_bd()
        self.cursor.execute(""" SELECT idVendedor FROM vendedor WHERE pnomeVendedor LIKE '%s'""" % (self.vendedorVenda))
        vend = self.cursor.fetchall()
        vend1= vend[0]
        self.cursor.execute("""INSERT INTO venda (idVenda, valor, dataVenda, idVendedor, cpf)
            VALUES (%s, %s, %s, %s, %s);""", (self.idVenda, self.valor, self.dataVenda, vend1[0], self.clienteVenda))
        self.conn.commit()
        self.desconectar_bd()
        self.select_vendasLista()
        self.limpa_tela3()
    def deleta_venda(self):
        self.idVenda = self.entry_idVenda.get()
        self.conexao_bd()
        self.cursor.execute("""DELETE FROM venda WHERE idVenda = %s""" % (self.idVenda))
        self.conn.commit()
        self.desconectar_bd()
        self.select_vendasLista()
        self.limpa_tela2()
        self.variaveisClientes()
        self.conexao_bd()
        self.cursor.execute("""UPDATE cliente SET pnomeCliente = %s, mnomeCliente = %s, unomeCliente = %s, email = %s, telefone = %s, endereco = %s WHERE cpf = %s""", 
            (self.nomeCliente, self.mnomeCliente, self.unomeCliente, self.email, self.telefone, self.endereco, self.cpf)); 
        self.conn.commit()
        self.desconectar_bd()
        self.select_clientesLista()
        self.limpa_tela3()
    def busca_venda(self):
        self.conexao_bd()
        self.variaveisVendas()
        self.listaVendas.delete(*self.listaVendas.get_children())
        self.entry_cliente.insert(END, '%')
        cpfCliente = self.entry_cliente.get()
        self.cursor.execute("SELECT idVenda, pnomeCliente, mnomeCliente, valor, dataVenda, pnomeVendedor from (SELECT idVenda, cliente.cpf, pnomeCliente, mnomeCliente, valor, dataVenda, pnomeVendedor FROM cliente INNER JOIN (SELECT idVenda, valor, dataVenda, pnomeVendedor, cpf FROM venda INNER JOIN vendedor ON venda.idVendedor = vendedor.idVendedor) AS test ON cliente.cpf = test.cpf ORDER by pnomeCliente) AS quest WHERE quest.cpf LIKE '%s'" % cpfCliente)
        busca = self.cursor.fetchall()
        for i in busca:
            self.listaVendas.insert("", "end", values=i)
        self.desconectar_bd()
        self.limpa_tela2()
    def doubleClickVendas(self, event):
        self.conexao_bd()
        self.limpa_tela2()
        self.variaveisVendas()
        self.listaVendas.selection()

        for n in self.listaVendas.selection():
            col1, col2, col3, col4, col5, col6 = self.listaVendas.item(n, "values")
            self.entry_idVenda.insert(END, col1)
    
    ##FUNÇÕES ABA CLIENTES        -3
    def limpa_tela3(self):
        self.entry_nomeCliente.delete(0, END)
        self.entry_primeiroSobrenome.delete(0, END)
        self.entry_ultimoSobrenome.delete(0, END)
        self.entry_cpf.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_telefone.delete(0, END)
        self.entry_endereco.delete(0, END)
        self.select_clientesLista()
    def variaveisClientes(self):
        self.nomeCliente = self.entry_nomeCliente.get()
        self.mnomeCliente = self.entry_primeiroSobrenome.get()
        self.unomeCliente = self.entry_ultimoSobrenome.get()
        self.cpf = self.entry_cpf.get()
        self.email = self.entry_email.get()
        self.telefone = self.entry_telefone.get()
        self.endereco = self.entry_endereco.get()
    def select_clientesLista(self):
        self.listaClientes.delete(*self.listaClientes.get_children())
        self.conexao_bd()
        sql1 = "SELECT pnomeCliente, mnomeCliente, cpf, email, telefone, endereco FROM cliente  ORDER BY pnomeCliente"
        self.cursor.execute(sql1)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaClientes.insert("", "end", values=i)
        self.desconectar_bd()
    def doubleClickClientes(self, event):
        self.conexao_bd()
        self.limpa_tela3()
        self.variaveisClientes()
        self.listaClientes.selection()

        for n in self.listaClientes.selection():
            col1, col2, col3, col4, col5, col6 = self.listaClientes.item(n, "values")
            self.entry_nomeCliente.insert(END, col1)
            self.entry_primeiroSobrenome.insert(END, col2)
            self.cursor.execute("SELECT unomeCliente FROM cliente WHERE cpf = '%s'" % col3)
            sobrenome = self.cursor.fetchall()
            self.entry_ultimoSobrenome.insert(END, sobrenome)
            print(col3)
            self.entry_cpf.insert(END, col3)
            self.entry_email.insert(END, col4)
            self.entry_telefone.insert(END, col5)
            self.entry_endereco.insert(END, col6)
    def add_novoCliente(self):
        self.variaveisClientes()
        self.conexao_bd()
        self.cursor.execute("""INSERT INTO cliente (pnomeCliente, mnomeCliente, unomeCliente, cpf, email, telefone, endereco)
            VALUES (%s, %s, %s, %s, %s, %s, %s);""", (self.nomeCliente, self.mnomeCliente, self.unomeCliente, self.cpf, self.email, self.telefone, self.endereco))
        self.conn.commit()
        self.desconectar_bd()
        self.select_clientesLista()
        self.limpa_tela3()
    def deleta_cliente(self):
        self.cpf = self.entry_cpf.get()
        self.conexao_bd()
        self.cursor.execute("""DELETE FROM cliente WHERE cpf = %s""" % (self.cpf))
        self.conn.commit()
        self.desconectar_bd()
        self.select_clientesLista()
        self.limpa_tela3()
    def altera_cliente(self):
        self.variaveisClientes()
        self.conexao_bd()
        self.cursor.execute("""UPDATE cliente SET pnomeCliente = %s, mnomeCliente = %s, unomeCliente = %s, email = %s, telefone = %s, endereco = %s WHERE cpf = %s""", 
            (self.nomeCliente, self.mnomeCliente, self.unomeCliente, self.email, self.telefone, self.endereco, self.cpf)); 
        self.conn.commit()
        self.desconectar_bd()
        self.select_clientesLista()
        self.limpa_tela3()
    def busca_cliente(self):
        self.conexao_bd()
        self.variaveisClientes()
        self.listaClientes.delete(*self.listaClientes.get_children())
        self.entry_nomeCliente.insert(END, '%')
        nome = self.entry_nomeCliente.get()
        self.cursor.execute(""" SELECT pnomeCliente, mnomeCliente, cpf, email, telefone, endereco FROM cliente WHERE pnomeCliente LIKE '%s' ORDER BY pnomecliente""" % (nome))
        busca = self.cursor.fetchall()
        for i in busca:
            self.listaClientes.insert("", "end", values=i)
        self.desconectar_bd()
        self.limpa_tela3()
    
    ##FUNÇÕES ABA MODULOS E INVERSORES        -4
    def limpa_tela4(self):
        self.entry_codMod.delete(0, END)
        self.entry_marcaMod.delete(0, END)
        self.entry_potMod.delete(0, END)
        self.entry_modeloMod.delete(0, END)
        self.entry_codInv.delete(0, END)
        self.entry_marcaInv.delete(0, END)
        self.entry_potInv.delete(0, END)
        self.entry_modeloInv.delete(0, END)
        self.select_modulosListaCad()
        self.select_inversoresListaCad()
    def variaveisModulos(self):
        self.codMod = self.entry_codMod.get()
        self.marcaMod = self.entry_marcaMod.get()
        self.potMod = self.entry_potMod.get()
        self.modeloMod = self.entry_modeloMod.get()
    def variaveisInversores(self):
        self.codInv = self.entry_codInv.get()
        self.marcaInv = self.entry_marcaInv.get()
        self.potInv = self.entry_potInv.get()
        self.modeloInv = self.entry_modeloInv.get()
    def select_modulosLista(self):
        self.listaModulos.delete(*self.listaModulos.get_children())
        self.conexao_bd()
        sql1 = "SELECT idProjeto, marcaModulo, potModulo, qtdModulo FROM modulo INNER JOIN registromodulos ON modulo.codModulo = registromodulos.codModulo  ORDER BY marcaModulo"
        self.cursor.execute(sql1)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaModulos.insert("", "end", values=i)
        self.desconectar_bd()
    def select_modulosListaCad(self):
        self.listaModulosCad.delete(*self.listaModulosCad.get_children())
        self.conexao_bd()
        sql1 = "SELECT codModulo, marcaModulo, potModulo, modeloModulo FROM modulo ORDER BY codModulo"
        self.cursor.execute(sql1)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaModulosCad.insert("", "end", values=i)
        self.desconectar_bd()
    def select_inversoresLista(self):
        self.listaInversores.delete(*self.listaInversores.get_children())
        self.conexao_bd()
        sql = "SELECT idProjeto, marcaInversor, potInversor, qtdInversor FROM inversor INNER JOIN registroinversor ON inversor.codInversor = registroinversor.codinversor  ORDER BY marcaInversor"
        self.cursor.execute(sql)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaInversores.insert("", "end", values=i)
        self.desconectar_bd()
    def select_inversoresListaCad(self):
        self.listaInversoresCad.delete(*self.listaInversoresCad.get_children())
        self.conexao_bd()
        sql1 = "SELECT codInversor, marcaInversor, potInversor, modeloInversor FROM inversor ORDER BY codInversor"
        self.cursor.execute(sql1)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaInversoresCad.insert("", "end", values=i)
        self.desconectar_bd()
    def add_novoModulo(self):
        self.variaveisModulos()
        self.conexao_bd()
        self.cursor.execute("""INSERT INTO modulo VALUES (%s, %s, %s, %s);""", (self.codMod, self.marcaMod, self.potMod, self.modeloMod))
        self.conn.commit()
        self.desconectar_bd()
        self.select_modulosListaCad()
        self.limpa_tela4()
    def add_novoInversor(self):
        self.variaveisInversores()
        self.conexao_bd()
        self.cursor.execute("""INSERT INTO inversor VALUES (%s, %s, %s, %s);""", (self.codInv, self.marcaInv, self.potInv, self.modeloInv))
        self.conn.commit()
        self.desconectar_bd()
        self.select_inversoresListaCad()
        self.limpa_tela4()
    def altera_modulo(self):
        self.variaveisModulos()
        self.conexao_bd()
        self.cursor.execute("""UPDATE modulo SET marcaModulo = %s, potModulo = %s, modeloModulo = %s WHERE codModulo = %s""", 
            (self.marcaMod, self.potMod, self.modeloMod, self.codMod)); 
        self.conn.commit()
        self.desconectar_bd()
        self.select_modulosListaCad()
        self.limpa_tela4()
    def altera_inversor(self):
        self.variaveisInversores()
        self.conexao_bd()
        self.cursor.execute("""UPDATE inversor SET marcaInversor = %s, potInversor = %s, modeloInversor = %s WHERE codInversor = %s""", 
            (self.marcaInv, self.potInv, self.modeloInv, self.codInv)); 
        self.conn.commit()
        self.desconectar_bd()
        self.select_inversoresListaCad()
        self.limpa_tela4()
    def deleta_modulo(self):
        self.codMod = self.entry_codMod.get()
        self.conexao_bd()
        self.cursor.execute("""DELETE FROM modulo WHERE codModulo = %s""" % (self.codMod))
        self.conn.commit()
        self.desconectar_bd()
        self.select_modulosListaCad()
        self.limpa_tela4()
    def deleta_inversor(self):
        self.codInv = self.entry_codInv.get()
        self.conexao_bd()
        self.cursor.execute("""DELETE FROM inversor WHERE codInversor = %s""" % (self.codInv))
        self.conn.commit()
        self.desconectar_bd()
        self.select_inversoresListaCad()
        self.limpa_tela4()

    ##FUNÇÕES ABA MONITORAMENTO        -5
    def limpa_tela5(self):
        self.entry_login.delete(0, END)
        self.entry_senha.delete(0, END)
        self.entry_plataforma.delete(0, END)
        self.entry_IDPROJ.delete(0, END)
        self.select_monitoramento()
    def variaveisMonitoramento(self):
        self.login = self.entry_login.get()
        self.senha = self.entry_senha.get()
        self.plataforma = self.entry_plataforma.get()
        self.idProj = self.entry_IDPROJ.get()
    def select_monitoramento(self):
        self.listaMonitoramento.delete(*self.listaMonitoramento.get_children())
        self.conexao_bd()
        sql1 = """SELECT pnomeCliente, mnomeCliente, login, senha, plataforma, marcaInversor FROM (SELECT login, senha, plataforma, marcaInversor, idProjeto FROM inversor INNER JOIN (
            SELECT login, senha, plataforma, codInversor, idProjeto FROM registroinversor INNER JOIN monitoramento ON monitoramento.login = registroInversor.snInversor) AS ASD 
            ON ASD. codInversor = inversor.codInversor) AS primeiro INNER JOIN (SELECT pnomeCLiente, mnomeCliente, idProjeto FROM cliente INNER JOIN (SELECT idProjeto, cpf FROM venda INNER JOIN projeto ON venda.idVenda = projeto.idVenda) AS ASP
            ON ASP.cpf = cliente.cpf) AS segundo ON primeiro.idProjeto = segundo.idProjeto;"""
        self.cursor.execute(sql1)
        lista = self.cursor.fetchall()
        for i in lista:
            self.listaMonitoramento.insert("", "end", values=i)
        self.desconectar_bd()
    def add_add_novoMonitoramento(self):
        self.variaveisMonitoramento()
        self.conexao_bd()
        self.cursor.execute("""SELECT snInversor FROM registroinversor WHERE idProjeto = '%s'""" % (self.idProj))
        login_id = self.cursor.fetchall()
        print(login_id)
        login_id1 = login_id[0]
        print(login_id1)
        self.cursor.execute("""INSERT INTO monitoramento VALUES (%s, %s, %s);""", (login_id1[0], self.senha, self.plataforma))
        self.conn.commit()
        self.desconectar_bd()
        self.select_modulosListaCad()
        self.limpa_tela5()

        self.codMod = self.entry_codMod.get()
        self.conexao_bd()
        self.cursor.execute("""DELETE FROM modulo WHERE codModulo = %s""" % (self.codMod))
        self.conn.commit()
        self.desconectar_bd()
        self.select_modulosListaCad()
        self.limpa_tela4()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.widgets_aba2()
        self.widgets_aba3()
        self.widgets_aba4()
        self.widgets_aba5()
        self.select_projetosLista()
        self.select_vendasLista()
        self.select_clientesLista()
        self.select_modulosLista()
        self.select_modulosListaCad()
        self.select_inversoresLista()
        self.select_inversoresListaCad()
        ##self.select_monitoramento()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro")
        self.root.configure(background="lightblue")
        self.root.geometry("1000x500")
        self.root.resizable(True, True)
        self.root.minsize(width=700, height=500)
    def frames(self):
        self.frame1 = Frame(self.root, border=4, bg="white", highlightbackground="grey", highlightthickness=2)
        self.frame1.place(relx= 0.02, rely=0.02, relwidth= 0.98, relheight=0.98) 
    def widgets_frame1(self):
        self.abas = ttk.Notebook(self.frame1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba3 = Frame(self.abas)
        self.aba4 = Frame(self.abas)
        self.aba5 = Frame(self.abas)
        self.aba6 = Frame(self.abas)

        self.aba1.configure(bg="lightblue")
        self.aba2.configure(bg="blue")
        self.aba3.configure(bg="lightblue")
        self.aba4.configure(bg="blue")
        self.aba5.configure(bg="lightblue")
        self.aba6.configure(bg="blue")

        self.abas.add(self.aba1, text='Projetos')
        self.abas.add(self.aba2, text='Vendas')
        self.abas.add(self.aba3, text='Clientes')
        self.abas.add(self.aba4, text='Produtos')
        self.abas.add(self.aba5, text='Monitoramento')
        self.abas.add(self.aba6, text='Outros')
        self.abas.place(relx= 0, rely=0, relwidth= 0.98, relheight= 0.98)

        ##  ABA 1
        self.btn_limpar = Button(self.aba1, text= "Limpar", command=self.limpa_tela1)
        self.btn_limpar.place(relx= 0.85, rely=0.05, relwidth= 0.1, relheight= 0.05)

        self.btn_buscar = Button(self.aba1, text= "Buscar", command=self.busca_projeto)
        self.btn_buscar.place(relx= 0.85, rely=0.12, relwidth= 0.1, relheight= 0.05)

        self.btn_novo = Button(self.aba1, text= "Novo", command=self.add_projeto)
        self.btn_novo.place(relx= 0.85, rely=0.19, relwidth= 0.1, relheight= 0.05)
        
        self.btn_alterar = Button(self.aba1, text= "Alterar", command=self.altera_projeto)
        self.btn_alterar.place(relx= 0.85, rely=0.26, relwidth= 0.1, relheight= 0.05)
        
        self.btn_excluir = Button(self.aba1, text= "Excluir", command=self.deleta_projeto)
        self.btn_excluir.place(relx= 0.85, rely=0.33, relwidth= 0.1, relheight= 0.05)


        self.lb_cod = Label(self.aba1, text= "ID Projeto")
        self.lb_cod.place(relx=0.05, rely=0.05)
        self.entry_cod = Entry(self.aba1)
        self.entry_cod.place(relx= 0.05,rely=0.1, relwidth=0.09)

        self.lb_pot = Label(self.aba1, text= "Potência do Sistema")
        self.lb_pot.place(relx=0.17, rely=0.05)
        self.entry_pot = Entry(self.aba1)
        self.entry_pot.place(relx= 0.17,rely=0.1, relwidth=0.15)

        self.lb_data = Label(self.aba1, text= "Data de Instalação")
        self.lb_data.place(relx=0.35, rely=0.05)
        self.entry_data = Entry(self.aba1)
        self.entry_data.place(relx= 0.35,rely=0.1, relwidth=0.1)

        self.lb_venda = Label(self.aba1, text= "Venda")
        self.lb_venda.place(relx=0.5, rely=0.05)
        self.entry_venda = Entry(self.aba1)
        self.entry_venda.place(relx= 0.5,rely=0.1, relwidth=0.09)

        self.lb_concessionaria = Label(self.aba1, text= "Concessionaria")
        self.lb_concessionaria.place(relx=0.65, rely=0.05)
        self.Tipvar1 = StringVar(self.aba1)
        self.TipV1 = ('CEEE', 'RGE')
        self.Tipvar1.set ('CEEE')
        self.popupMenu1 = OptionMenu(self.aba1, self.Tipvar1, *self.TipV1)
        self.popupMenu1.place(relx= 0.65, rely=0.1, relwidth= 0.15, relheight= 0.05)

        self.lb_ligacao = Label(self.aba1, text= "Tipo de Ligação")
        self.lb_ligacao.place(relx=0.05, rely=0.2)
        self.Tipvar2 = StringVar(self.aba1)
        self.TipV2 = ('Monofasica', 'Bifasica', 'Trifasica')
        self.Tipvar2.set ('MONOFASICA')
        self.popupMenu2 = OptionMenu(self.aba1, self.Tipvar2, *self.TipV2)
        self.popupMenu2.place(relx= 0.05, rely=0.25, relwidth= 0.18, relheight= 0.05)

        self.lb_uc = Label(self.aba1, text= "UC Geradora")
        self.lb_uc.place(relx=0.25, rely=0.2)
        self.entry_uc = Entry(self.aba1)
        self.entry_uc.place(relx= 0.25,rely=0.25, relwidth=0.2)

        self.lb_engenheiro = Label(self.aba1, text= "Engenheiro")
        self.lb_engenheiro.place(relx=0.5, rely=0.2)
        self.Tipvar3 = StringVar(self.aba1)
        self.TipV3 = ('A', 'B', 'C')
        self.Tipvar3.set ('A')
        self.popupMenu3 = OptionMenu(self.aba1, self.Tipvar3, *self.TipV3)
        self.popupMenu3.place(relx= 0.5, rely=0.25, relwidth= 0.18, relheight= 0.05)

        self.lb_snInversor = Label(self.aba1, text= "SN Inversor")
        self.lb_snInversor.place(relx=0.05, rely=0.35)
        self.entry_SN = Entry(self.aba1)
        self.entry_SN.place(relx= 0.13,rely=0.35, relwidth=0.12)

        self.lb_codInversor = Label(self.aba1, text= "Código Inversor")
        self.lb_codInversor.place(relx=0.27, rely=0.35)
        self.entry_codInversor = Entry(self.aba1)
        self.entry_codInversor.place(relx= 0.37,rely=0.35, relwidth=0.07)

        self.lb_qtdInversor = Label(self.aba1, text= "Quantidade")
        self.lb_qtdInversor.place(relx=0.5, rely=0.35)
        self.entry_qtdInversor = Entry(self.aba1)
        self.entry_qtdInversor.place(relx= 0.58,rely=0.35, relwidth=0.09)

        self.lb_codModulos = Label(self.aba1, text= "Código Módulo")
        self.lb_codModulos.place(relx=0.05, rely=0.45)
        self.entry_codModulos = Entry(self.aba1)
        self.entry_codModulos.place(relx= 0.15,rely=0.45, relwidth=0.09)

        self.lb_qtdModulos = Label(self.aba1, text= "Quantidade")
        self.lb_qtdModulos.place(relx=0.28, rely=0.45)
        self.entry_qtdModulos = Entry(self.aba1)
        self.entry_qtdModulos.place(relx= 0.36,rely=0.45, relwidth=0.09)

        self.listaProjetos = ttk.Treeview(self.aba1, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))
        self.listaProjetos.heading("#0", text="")
        self.listaProjetos.heading("#1", text="ID")
        self.listaProjetos.heading("#2", text="Potência")
        self.listaProjetos.heading("#3", text="Data Instalação")
        self.listaProjetos.heading("#4", text="Concessionaria")
        self.listaProjetos.heading("#5", text="Tipo de Ligação")
        self.listaProjetos.heading("#6", text="UC")
        self.listaProjetos.heading("#7", text="ID Venda")
        self.listaProjetos.heading("#8", text="Crea")

        self.listaProjetos.column("#0", width=5)
        self.listaProjetos.column("#1", width=5)
        self.listaProjetos.column("#2", width=15)
        self.listaProjetos.column("#3", width=60)
        self.listaProjetos.column("#4", width=60)
        self.listaProjetos.column("#5", width=50)
        self.listaProjetos.column("#6", width=30)
        self.listaProjetos.column("#7", width=15)
        self.listaProjetos.column("#8", width=30)

        self.listaProjetos.place(relx=0.02, rely=0.55, relwidth=0.91, relheight=0.4)
        
        self.scroolLista = Scrollbar(self.aba1, orient='vertical')
        self.listaProjetos.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.93, rely=0.55, relwidth=0.03, relheight=0.4)
        self.listaProjetos.bind("<Double-1>", self.doubleClickProjetos)    
    def widgets_aba2(self):
        ##  ABA 2
        self.btn_cadastrar = Button(self.aba2, text= "Cadastrar", command=self.add_novaVenda)
        self.btn_cadastrar.place(relx= 0.85, rely=0.05, relwidth= 0.1, relheight= 0.05)

        self.btn_excluirVenda = Button(self.aba2, text= "Excluir", command=self.deleta_venda)
        self.btn_excluirVenda.place(relx= 0.85, rely=0.12, relwidth= 0.1, relheight= 0.05)

        self.btn_buscarVenda = Button(self.aba2, text= "Buscar", command=self.busca_venda)
        self.btn_buscarVenda.place(relx= 0.85, rely=0.19, relwidth= 0.1, relheight= 0.05)

        self.btn_limpar = Button(self.aba2, text= "Limpar", command=self.limpa_tela2)
        self.btn_limpar.place(relx= 0.85, rely=0.26, relwidth= 0.1, relheight= 0.05)

        self.lb_idVenda = Label(self.aba2, text= "ID Venda")
        self.lb_idVenda.place(relx=0.05, rely=0.05)
        self.entry_idVenda = Entry(self.aba2)
        self.entry_idVenda.place(relx= 0.05,rely=0.1, relwidth=0.2)

        self.lb_valor = Label(self.aba2, text= "Valor")
        self.lb_valor.place(relx=0.30, rely=0.05)
        self.entry_valor = Entry(self.aba2)
        self.entry_valor.place(relx= 0.30,rely=0.1, relwidth=0.2)

        self.lb_dataVenda = Label(self.aba2, text= "Data de Venda")
        self.lb_dataVenda.place(relx=0.55, rely=0.05)
        self.entry_dataVenda = Entry(self.aba2)
        self.entry_dataVenda.place(relx= 0.55,rely=0.1, relwidth=0.2)

        self.lb_vendedor = Label(self.aba2, text= "Vendedor")
        self.lb_vendedor.place(relx=0.05, rely=0.20)
        self.entry_vendedorVenda = Entry(self.aba2)
        self.entry_vendedorVenda.place(relx= 0.05,rely=0.25, relwidth=0.2)

        self.lb_cliente = Label(self.aba2, text= "Cliente")
        self.lb_cliente.place(relx=0.30, rely=0.20)
        self.entry_cliente = Entry(self.aba2)
        self.entry_cliente.place(relx= 0.30,rely=0.25, relwidth=0.2)

        self.listaVendas = ttk.Treeview(self.aba2, height=4, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaVendas.heading("#0", text="")
        self.listaVendas.heading("#1", text="ID Venda")
        self.listaVendas.heading("#2", text="Nome")
        self.listaVendas.heading("#3", text="Sobrenome")
        self.listaVendas.heading("#4", text="Valor")
        self.listaVendas.heading("#5", text="Data")
        self.listaVendas.heading("#6", text="Vendedor")

        self.listaVendas.column("#0", width=1)
        self.listaVendas.column("#1", width=5)
        self.listaVendas.column("#2", width=5)
        self.listaVendas.column("#3", width=5)
        self.listaVendas.column("#4", width=5)
        self.listaVendas.column("#5", width=5)
        self.listaVendas.column("#6", width=5)

        self.listaVendas.place(relx=0.02, rely=0.55, relwidth=0.91, relheight=0.4)
        
        self.scroolLista = Scrollbar(self.aba2, orient='vertical')
        self.listaVendas.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.93, rely=0.55, relwidth=0.03, relheight=0.4)
        self.listaVendas.bind("<Double-1>", self.doubleClickVendas) 
    def widgets_aba3(self):
        self.btn_limpar = Button(self.aba3, text= "Limpar", command=self.limpa_tela3)
        self.btn_limpar.place(relx= 0.85, rely=0.05, relwidth= 0.1, relheight= 0.05)

        self.btn_buscar = Button(self.aba3, text= "Buscar", command=self.busca_cliente)
        self.btn_buscar.place(relx= 0.85, rely=0.12, relwidth= 0.1, relheight= 0.05)

        self.btn_novo = Button(self.aba3, text= "Novo", command=self.add_novoCliente)
        self.btn_novo.place(relx= 0.85, rely=0.19, relwidth= 0.1, relheight= 0.05)
        
        self.btn_alterar = Button(self.aba3, text= "Alterar", command=self.altera_cliente)
        self.btn_alterar.place(relx= 0.85, rely=0.26, relwidth= 0.1, relheight= 0.05)
        
        self.btn_excluir = Button(self.aba3, text= "Excluir", command=self.deleta_cliente)
        self.btn_excluir.place(relx= 0.85, rely=0.33, relwidth= 0.1, relheight= 0.05)

        self.lb_nomeCliente = Label(self.aba3, text= "Nome")
        self.lb_nomeCliente.place(relx=0.05, rely=0.05)
        self.entry_nomeCliente = Entry(self.aba3)
        self.entry_nomeCliente.place(relx= 0.05,rely=0.1, relwidth=0.2)

        self.lb_primeiroSobrenome = Label(self.aba3, text= "Primeiro Sobrenome")
        self.lb_primeiroSobrenome.place(relx=0.30, rely=0.05)
        self.entry_primeiroSobrenome = Entry(self.aba3)
        self.entry_primeiroSobrenome.place(relx= 0.30,rely=0.1, relwidth=0.2)

        self.lb_ultimoSobrenome = Label(self.aba3, text= "Último Sobrenome")
        self.lb_ultimoSobrenome.place(relx=0.55, rely=0.05)
        self.entry_ultimoSobrenome = Entry(self.aba3)
        self.entry_ultimoSobrenome.place(relx= 0.55,rely=0.1, relwidth=0.2)

        self.lb_cpf = Label(self.aba3, text= "CPF")
        self.lb_cpf.place(relx=0.05, rely=0.20)
        self.entry_cpf = Entry(self.aba3)
        self.entry_cpf.place(relx= 0.05,rely=0.25, relwidth=0.2)

        self.lb_email = Label(self.aba3, text= "E-mail")
        self.lb_email.place(relx=0.3, rely=0.2)
        self.entry_email = Entry(self.aba3)
        self.entry_email.place(relx= 0.3,rely=0.25, relwidth=0.4)

        self.lb_telefone = Label(self.aba3, text= "Telefone")
        self.lb_telefone.place(relx=0.05, rely=0.35)
        self.entry_telefone = Entry(self.aba3)
        self.entry_telefone.place(relx= 0.05,rely=0.4, relwidth=0.2)

        self.lb_endereco = Label(self.aba3, text= "Endereço")
        self.lb_endereco.place(relx=0.3, rely=0.35)
        self.entry_endereco = Entry(self.aba3)
        self.entry_endereco.place(relx= 0.3,rely=0.4, relwidth=0.4)

        self.listaClientes = ttk.Treeview(self.aba3, height=4, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaClientes.heading("#0", text="")
        self.listaClientes.heading("#1", text="Nome")
        self.listaClientes.heading("#2", text="Sobrenome")
        self.listaClientes.heading("#3", text="CPF")
        self.listaClientes.heading("#4", text="E-mail")
        self.listaClientes.heading("#5", text="Telefone")
        self.listaClientes.heading("#6", text="Endereço")

        self.listaClientes.column("#0", width=1)
        self.listaClientes.column("#1", width=5)
        self.listaClientes.column("#2", width=5)
        self.listaClientes.column("#3", width=5)
        self.listaClientes.column("#4", width=5)
        self.listaClientes.column("#5", width=5)
        self.listaClientes.column("#6", width=5)
        self.listaClientes.place(relx=0.02, rely=0.55, relwidth=0.91, relheight=0.4)
        
        self.scroolLista = Scrollbar(self.aba3, orient='vertical')
        self.listaClientes.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.93, rely=0.55, relwidth=0.03, relheight=0.4)
        self.listaClientes.bind("<Double-1>", self.doubleClickClientes) 
    def widgets_aba4(self):
        self.lb_inv = Label(self.aba4, text= "Módulos")
        self.lb_inv.place(relx=0.15, rely=0.05)

        self.lb_mod = Label(self.aba4, text= "Inversores")
        self.lb_mod.place(relx=0.65, rely=0.05)

        self.btn_cadastrarMod = Button(self.aba4, text= "Cadastrar", command=self.add_novoModulo)
        self.btn_cadastrarMod.place(relx= 0.35, rely=0.16, relwidth= 0.1, relheight= 0.05)

        self.btn_alterarMod = Button(self.aba4, text= "Alterar", command=self.altera_modulo)
        self.btn_alterarMod.place(relx= 0.35, rely=0.23, relwidth= 0.1, relheight= 0.05)

        self.btn_excluirMod = Button(self.aba4, text= "Excluir", command=self.deleta_modulo)
        self.btn_excluirMod.place(relx= 0.35, rely=0.3, relwidth= 0.1, relheight= 0.05)

        self.btn_cadastrarInv = Button(self.aba4, text= "Cadastrar", command=self.add_novoInversor)
        self.btn_cadastrarInv.place(relx= 0.85, rely=0.16, relwidth= 0.1, relheight= 0.05)

        self.btn_alterarInv = Button(self.aba4, text= "Alterar", command=self.altera_inversor)
        self.btn_alterarInv.place(relx= 0.85, rely=0.23, relwidth= 0.1, relheight= 0.05)

        self.btn_excluirInv = Button(self.aba4, text= "Excluir", command=self.deleta_inversor)
        self.btn_excluirInv.place(relx= 0.85, rely=0.3, relwidth= 0.1, relheight= 0.05)

        # campos MODULO
        self.lb_codMod = Label(self.aba4, text= "Código")
        self.lb_codMod.place(relx=0.04, rely=0.12)
        self.entry_codMod = Entry(self.aba4)
        self.entry_codMod.place(relx= 0.1,rely=0.12, relwidth=0.2)

        self.lb_marcaMod = Label(self.aba4, text= "Marca")
        self.lb_marcaMod.place(relx=0.04, rely=0.2)
        self.entry_marcaMod = Entry(self.aba4)
        self.entry_marcaMod.place(relx= 0.1,rely=0.2, relwidth=0.2)

        self.lb_potMod = Label(self.aba4, text= "Potência")
        self.lb_potMod.place(relx=0.04, rely=0.28)
        self.entry_potMod = Entry(self.aba4)
        self.entry_potMod.place(relx= 0.1,rely=0.28, relwidth=0.2)

        self.lb_modeloMod = Label(self.aba4, text= "Modelo")
        self.lb_modeloMod.place(relx=0.04, rely=0.36)
        self.entry_modeloMod = Entry(self.aba4)
        self.entry_modeloMod.place(relx= 0.1,rely=0.36, relwidth=0.2)

        ## campos INVERSOR
        self.lb_codInv = Label(self.aba4, text= "Código")
        self.lb_codInv.place(relx=0.54, rely=0.12)
        self.entry_codInv = Entry(self.aba4)
        self.entry_codInv.place(relx= 0.6,rely=0.12, relwidth=0.2)

        self.lb_marcaInv = Label(self.aba4, text= "Marca")
        self.lb_marcaInv.place(relx=0.54, rely=0.2)
        self.entry_marcaInv = Entry(self.aba4)
        self.entry_marcaInv.place(relx= 0.6,rely=0.2, relwidth=0.2)

        self.lb_potInv = Label(self.aba4, text= "Potência")
        self.lb_potInv.place(relx=0.54, rely=0.28)
        self.entry_potInv = Entry(self.aba4)
        self.entry_potInv.place(relx= 0.6,rely=0.28, relwidth=0.2)

        self.lb_modeloInv = Label(self.aba4, text= "Modelo")
        self.lb_modeloInv.place(relx=0.54, rely=0.36)
        self.entry_modeloInv = Entry(self.aba4)
        self.entry_modeloInv.place(relx= 0.6,rely=0.36, relwidth=0.2)

        ##LISTA MODULOS PRODUTOS
        self.listaModulosCad = ttk.Treeview(self.aba4, height=4, column=("col1", "col2", "col3", "col4"))
        self.listaModulosCad.heading("#0", text="Produtos")
        self.listaModulosCad.heading("#1", text="Código")
        self.listaModulosCad.heading("#2", text="Marca")
        self.listaModulosCad.heading("#3", text="Potencia(w)")
        self.listaModulosCad.heading("#4", text="Modelo")

        self.listaModulosCad.column("#0", width=1)
        self.listaModulosCad.column("#1", width=5)
        self.listaModulosCad.column("#2", width=5)
        self.listaModulosCad.column("#3", width=5)
        self.listaModulosCad.column("#4", width=5)
        self.listaModulosCad.place(relx=0.02, rely=0.5, relwidth=0.44, relheight=0.2)
        self.scroolLista = Scrollbar(self.aba4, orient='vertical')
        self.listaModulosCad.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.46, rely=0.5, relwidth=0.02, relheight=0.2)

        ##LISTA INVERSORES PRODUTOS
        self.listaInversoresCad = ttk.Treeview(self.aba4, height=4, column=("col1", "col2", "col3", "col4"))
        self.listaInversoresCad.heading("#0", text="Produtos")
        self.listaInversoresCad.heading("#1", text="Código")
        self.listaInversoresCad.heading("#2", text="Marca")
        self.listaInversoresCad.heading("#3", text="Potencia(kwp)")
        self.listaInversoresCad.heading("#4", text="Modelo")

        self.listaInversoresCad.column("#0", width=1)
        self.listaInversoresCad.column("#1", width=5)
        self.listaInversoresCad.column("#2", width=5)
        self.listaInversoresCad.column("#3", width=5)
        self.listaInversoresCad.column("#4", width=5)
        self.listaInversoresCad.place(relx=0.52, rely=0.5, relwidth=0.44, relheight=0.2)
        self.scroolLista = Scrollbar(self.aba4, orient='vertical')
        self.listaInversoresCad.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.5, relwidth=0.02, relheight=0.2)

        ##LISTA MODULOS VENDIDOS
        self.listaModulos = ttk.Treeview(self.aba4, height=4, column=("col1", "col2", "col3", "col4"))
        self.listaModulos.heading("#0", text="Vendidos")
        self.listaModulos.heading("#1", text="ID Projeto")
        self.listaModulos.heading("#2", text="Marca")
        self.listaModulos.heading("#3", text="Potencia(w)")
        self.listaModulos.heading("#4", text="Qtd")

        self.listaModulos.column("#0", width=1)
        self.listaModulos.column("#1", width=5)
        self.listaModulos.column("#2", width=5)
        self.listaModulos.column("#3", width=5)
        self.listaModulos.column("#4", width=5)
        self.listaModulos.place(relx=0.02, rely=0.7, relwidth=0.44, relheight=0.3)
        
        self.scroolLista = Scrollbar(self.aba4, orient='vertical')
        self.listaModulos.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.46, rely=0.7, relwidth=0.02, relheight=0.3)

        ##LISTA INVERSORES VENDIDOS
        self.listaInversores = ttk.Treeview(self.aba4, height=4, column=("col1", "col2", "col3", "col4"))
        self.listaInversores.heading("#0", text="Vendidos")
        self.listaInversores.heading("#1", text="ID Projeto")
        self.listaInversores.heading("#2", text="Marca")
        self.listaInversores.heading("#3", text="Potencia(kwp)")
        self.listaInversores.heading("#4", text="Qtd")

        self.listaInversores.column("#0", width=1)
        self.listaInversores.column("#1", width=5)
        self.listaInversores.column("#2", width=5)
        self.listaInversores.column("#3", width=5)
        self.listaInversores.column("#4", width=5)
        self.listaInversores.place(relx=0.52, rely=0.7, relwidth=0.44, relheight=0.3)
        
        self.scroolLista = Scrollbar(self.aba4, orient='vertical')
        self.listaInversores.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.7, relwidth=0.02, relheight=0.3) 
    def widgets_aba5(self):
        self.btn_buscarLogin = Button(self.aba5, text= "Buscar")
        self.btn_buscarLogin.place(relx= 0.8, rely=0.05, relwidth= 0.1, relheight= 0.05)

        self.btn_cadastrarMonitoramento = Button(self.aba5, text= "Cadastrar", command=self.add_add_novoMonitoramento)
        self.btn_cadastrarMonitoramento.place(relx= 0.35, rely=0.14, relwidth= 0.1, relheight= 0.05)

        self.btn_alterarMonitoramento = Button(self.aba5, text= "Alterar")
        self.btn_alterarMonitoramento.place(relx= 0.35, rely=0.2, relwidth= 0.1, relheight= 0.05)

        self.btn_excluirMonitoramento = Button(self.aba5, text= "Excluir")
        self.btn_excluirMonitoramento.place(relx= 0.35, rely=0.26, relwidth= 0.1, relheight= 0.05)

        self.lb_login = Label(self.aba5, text= "Login")
        self.lb_login.place(relx=0.04, rely=0.12)
        self.entry_login = Entry(self.aba5)
        self.entry_login.place(relx= 0.12, rely=0.12, relwidth=0.2)

        self.lb_senha = Label(self.aba5, text= "Senha")
        self.lb_senha.place(relx=0.04, rely=0.2)
        self.entry_senha = Entry(self.aba5)
        self.entry_senha.place(relx= 0.12, rely=0.2, relwidth=0.2)

        self.lb_plataforma = Label(self.aba5, text= "Plataforma")
        self.lb_plataforma.place(relx=0.04, rely=0.28)
        self.entry_plataforma = Entry(self.aba5)
        self.entry_plataforma.place(relx= 0.12, rely=0.28, relwidth=0.2)

        self.lb_idProjeto = Label(self.aba5, text= "ID Projeto")
        self.lb_idProjeto.place(relx=0.04, rely=0.36)
        self.entry_IDPROJ = Entry(self.aba5)
        self.entry_IDPROJ.place(relx= 0.12, rely=0.36, relwidth=0.2)

        self.listaMonitoramento = ttk.Treeview(self.aba5, height=4, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaMonitoramento.heading("#0", text="")
        self.listaMonitoramento.heading("#1", text="Nome")
        self.listaMonitoramento.heading("#2", text="Sobrenome")
        self.listaMonitoramento.heading("#3", text="Login")
        self.listaMonitoramento.heading("#4", text="Senha")
        self.listaMonitoramento.heading("#5", text="Plataforma")
        self.listaMonitoramento.heading("#6", text="Marca Inversor")

        self.listaMonitoramento.column("#0", width=1)
        self.listaMonitoramento.column("#1", width=5)
        self.listaMonitoramento.column("#2", width=5)
        self.listaMonitoramento.column("#3", width=5)
        self.listaMonitoramento.column("#4", width=5)
        self.listaMonitoramento.column("#5", width=5)
        self.listaMonitoramento.column("#6", width=5)
        self.listaMonitoramento.place(relx=0.02, rely=0.55, relwidth=0.91, relheight=0.4)
        
        self.scroolLista = Scrollbar(self.aba5, orient='vertical')
        self.listaMonitoramento.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.93, rely=0.55, relwidth=0.03, relheight=0.4)


Application()