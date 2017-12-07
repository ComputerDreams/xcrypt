#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xcrypt_3.0.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from subprocess import PIPE, Popen, run
import os

def out(command):
	result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
	return result.stdout+"\n"+result.stderr

### ASYMMETRIC ENCRYPTION

## GENERATE KEYS

def a_generate_keys():
	keyname = ui.a_g_keyname.text()
	if(keyname==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		if ui.a_g_signing.isChecked():
			ui.console.append("[INFO] Generate Encryption and Signing Keypair: "+keyname+"\n")
			output = out("ccr -g enc --name "+keyname)
			ui.console.append(output)
			output = out("ccr -g sig --name "+keyname)
			ui.console.append(output)
		else:
			ui.console.append("[INFO] Generate Encryption Keypair: "+keyname+"\n")
			output = out("ccr -g enc --name "+keyname)
			ui.console.append(output)

## SHOW KEYS

def a_show_public():
	output = out("ccr -k").strip().splitlines()
	if(len(output)==0):
		ui.console.append("[INFO] No Keys found.\n")
	else:
                ui.console.append("PUBLIC KEYS:")
                for line in output:
                    if "FMTSEQ128C-CUBE256-CUBE128" in line:
                        ui.console.append("Signing: "+line.replace("pubkey","").replace("MCEQCMDPC128FO-CUBE256-CHACHA20","").replace("FMTSEQ128C-CUBE256-CUBE128",""))
                    else:
                        ui.console.append("Encrypt: "+line.replace("pubkey","").replace("MCEQCMDPC128FO-CUBE256-CHACHA20",""))
                ui.console.append("")

def a_show_private():
	output = out("ccr -K").strip().splitlines()
	if(len(output)==0):
		ui.console.append("[INFO] No Keys found.\n")
	else:
                ui.console.append("PRIVATE KEYS:")
                for line in output:
                    if "FMTSEQ128C-CUBE256-CUBE128" in line:
                        ui.console.append("Signing: "+line.replace("keypair","").replace("MCEQCMDPC128FO-CUBE256-CHACHA20","").replace("FMTSEQ128C-CUBE256-CUBE128",""))
                    else:
                        ui.console.append("Encrypt: "+line.replace("keypair","").replace("MCEQCMDPC128FO-CUBE256-CHACHA20",""))
                ui.console.append("")

## RENAME KEYS

def a_rename_update():
    output = out("ccr -k").strip().splitlines()
    listing = []
    if(len(output)==0):
        ui.a_r_oldkey.clear()
        ui.console.append("[INFO] No Keys found.\n")
    else:
        for line in output:
            if "FMTSEQ128C-CUBE256-CUBE128" in line:
                pass
            else:
                listing.append(line.split()[-1])
        ui.a_r_oldkey.clear()
        ui.a_r_oldkey.addItems(listing)

def a_rename():
	old_name = ui.a_r_oldkey.currentText()
	new_name = ui.a_r_newkey.text()
	if(old_name=="" or new_name==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Renamed "+old_name+" to "+new_name+"\n")
		output = out("ccr -m "+old_name+" -N "+new_name)

## DELETE KEYS

def a_delete_update():
    output = out("ccr -k").strip().splitlines()
    listing = []
    if(len(output)==0):
        ui.a_d_keyname.clear()
        ui.console.append("[INFO] No Keys found.\n")
    else:
        for line in output:
            if "FMTSEQ128C-CUBE256-CUBE128" in line:
                pass
            else:
                listing.append(line.split()[-1])
        ui.a_d_keyname.clear()
        ui.a_d_keyname.addItems(listing)

def a_delete_pub():
	key = ui.a_d_keyname.currentText()
	if(key==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Removed Key: "+key+"\n")
		out("ccr --yes -x "+key)

def a_delete_priv():
	key = ui.a_d_keyname.currentText()
	if(key==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Removed Key: "+key+"\n")
		out("ccr --yes -X "+key)

## IMPORT KEYS

def a_import_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.a_i_keyname.setText(f)

def a_import_pub():
	filename = ui.a_i_keyname.text()
	if(filename==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Import: "+filename+"\n")
		out("ccr -i -a --yes -R "+filename)

def a_import_priv():
	filename = ui.a_i_keyname.text()
	if(filename==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Import: "+filename+"\n")
		out("ccr -I -a --yes -R "+filename)

## EXPORT KEYS

def a_export_update():
    output = out("ccr -k").strip().splitlines()
    listing = []
    if(len(output)==0):
        ui.a_e_keyname.clear()
        ui.console.append("[INFO] No Keys found.\n")
    else:
        for line in output:
            if "FMTSEQ128C-CUBE256-CUBE128" in line:
                pass
            else:
                listing.append(line.split()[-1])
        ui.a_e_keyname.clear()
        ui.a_e_keyname.addItems(listing)

def a_export_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.a_e_output.setText(f)

def a_export_pub():
	key = ui.a_e_keyname.currentText()
	output = ui.a_e_output.text()
	if(key=="" or output==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Exported Public Key: "+key+"\n")
		out("ccr -p -a --yes -o "+output+" -F "+key)

def a_export_priv():
	key = ui.a_e_keyname.currentText()
	output = ui.a_e_output.text()
	if(key=="" or output==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Export Private Key: "+key+"\n")
		out("ccr -P -a --yes -o "+output+" -F "+key)

## ENCRYPT FILE

def a_encrypt_update():
    output = out("ccr -k").strip().splitlines()
    listing = []
    if(len(output)==0):
        ui.a_enc_pubkey.clear()
        ui.console.append("[INFO] No Keys found.\n")
    else:
        for line in output:
            if "FMTSEQ128C-CUBE256-CUBE128" in line:
                pass
            else:
                listing.append(line.split()[-1])
        ui.a_enc_pubkey.clear()
        ui.a_enc_pubkey.addItems(listing)

def a_encrypt_in_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.a_enc_clear.setText(f)

def a_encrypt_out_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.a_enc_crypt.setText(f)

def a_encrypt():
	public = ui.a_enc_pubkey.currentText()
	clear = ui.a_enc_clear.text()
	crypt = ui.a_enc_crypt.text()
	if(public=="" or clear=="" or crypt==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		if ui.a_enc_sign.isChecked():
			out("ccr -esa -r "+public+" -o "+crypt+" < "+clear)
			ui.console.append("[INFO] File Encrypted and Signed.\n")
		else:
			out("ccr -ea -r "+public+" -o "+crypt+" < "+clear)
			ui.console.append("[INFO] File Encrypted.\n")

## DECRYPT FILE

def a_decrypt_update():
    output = out("ccr -K").strip().splitlines()
    listing = []
    if(len(output)==0):
        ui.a_dec_privkey.clear()
        ui.console.append("[INFO] No Keys found.\n")
    else:
        for line in output:
            if "FMTSEQ128C-CUBE256-CUBE128" in line:
                pass
            else:
                listing.append(line.split()[-1])
        ui.a_dec_privkey.clear()
        ui.a_dec_privkey.addItems(listing)

def a_decrypt_in_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.a_dec_crypt.setText(f)

def a_decrypt_out_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.a_dec_clear.setText(f)

def a_decrypt():
	private = ui.a_dec_privkey.currentText()
	crypt = ui.a_dec_crypt.text()
	clear = ui.a_dec_clear.text()
	if(private=="" or clear=="" or crypt==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		if ui.a_dec_verify.isChecked():
			output = out("ccr -dva -r "+private+" -o "+clear+" < "+crypt)
			ui.console.append(output)
			ui.console.append("[INFO] File Decrypted and Verified.\n")
		else:
			output = out("ccr -da -r "+private+" -o "+clear+" < "+crypt)
			ui.console.append(output)
			ui.console.append("[INFO] File Decrypted.\n")

### SYMMETRIC ENCRYPTION

## GENERATE KEY

def s_generate_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_g_keyname.setText(f)

def s_generate():
	keyname = ui.s_g_keyname.text()
	if(keyname==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Generating Key.\n")
		output = out("ccr -g sha256,chacha20 -aS "+keyname)

## ENCRYPT FILE

def s_enc_key_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_enc_keyfile.setText(f)

def s_enc_in_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_enc_clear.setText(f)

def s_enc_out_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_enc_crypt.setText(f)

def s_encrypt():
	key = ui.s_enc_keyfile.text()
	clear = ui.s_enc_clear.text()
	crypt = ui.s_enc_crypt.text()
	if(key=="" or clear=="" or crypt==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] File Encrypted.\n")
		output = out("ccr -eaS "+key+" -R "+clear+" -o "+crypt)

## DECRYPT FILE

def s_dec_key_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_dec_keyfile.setText(f)

def s_dec_in_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_dec_crypt.setText(f)

def s_dec_out_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_dec_clear.setText(f)

def s_decrypt():
	key = ui.s_dec_keyfile.text()
	crypt = ui.s_dec_crypt.text()
	clear = ui.s_dec_clear.text()
	if(key=="" or clear=="" or crypt==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] File Decrypted.\n")
		output = out("ccr -daS "+key+" -R "+crypt+" -o "+clear)

## GENERATE HASH

def s_hash_in_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_h_filename.setText(f)

def s_hash_out_dia():
	f,x=QFileDialog.getSaveFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_h_hash.setText(f)

def s_hash_generate():
	inputfile = ui.s_h_filename.text()
	hashfile = ui.s_h_hash.text()
	if(inputfile=="" or hashfile==""):
		ui.console.append("[ERROR] Check your Inputs.\n")
	else:
		ui.console.append("[INFO] Hash has been generated.\n")
		output = out("ccr -asS "+hashfile+" < "+inputfile)

## VERIFY HASH

def s_ver_in_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_v_filename.setText(f)

def s_ver_out_dia():
	f,x=QFileDialog.getOpenFileName()
	if " " in f:
		f = f.replace(" ","\ ")
	ui.s_v_hash.setText(f)

def s_hash_verify():
	inputfile = ui.s_v_filename.text()
	hashfile = ui.s_v_hash.text()
	if(inputfile=="" or hashfile==""):
		ui.console.append("[ERROR] Check your Inputs.\ņ")
	else:
		ui.console.append("[INFO] Verifying Hash.\n")
		output = out("ccr -avS "+hashfile+" < "+inputfile)
		ui.console.append(output)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(711, 501)
        MainWindow.setMinimumSize(QtCore.QSize(711, 501))
        MainWindow.setMaximumSize(QtCore.QSize(711, 501))
        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setObjectName("MainWidget")
        self.crypto_mode = QtWidgets.QTabWidget(self.MainWidget)
        self.crypto_mode.setGeometry(QtCore.QRect(0, 10, 711, 321))
        self.crypto_mode.setObjectName("crypto_mode")
        self.asymmetric = QtWidgets.QWidget()
        self.asymmetric.setObjectName("asymmetric")
        self.asymmetric_tabs = QtWidgets.QTabWidget(self.asymmetric)
        self.asymmetric_tabs.setGeometry(QtCore.QRect(0, 10, 701, 271))
        self.asymmetric_tabs.setObjectName("asymmetric_tabs")
        self.a_generate = QtWidgets.QWidget()
        self.a_generate.setObjectName("a_generate")
        self.label = QtWidgets.QLabel(self.a_generate)
        self.label.setGeometry(QtCore.QRect(10, 8, 281, 31))
        self.label.setObjectName("label")
        self.a_g_keyname = QtWidgets.QLineEdit(self.a_generate)
        self.a_g_keyname.setGeometry(QtCore.QRect(266, 7, 421, 32))
        self.a_g_keyname.setObjectName("a_g_keyname")
        self.a_g_signing = QtWidgets.QCheckBox(self.a_generate)
        self.a_g_signing.setGeometry(QtCore.QRect(10, 46, 671, 31))
        self.a_g_signing.setObjectName("a_g_signing")
        self.a_g_generate = QtWidgets.QPushButton(self.a_generate)
        self.a_g_generate.setGeometry(QtCore.QRect(0, 83, 691, 151))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_g_generate.setFont(font)
        self.a_g_generate.setObjectName("a_g_generate")
        self.asymmetric_tabs.addTab(self.a_generate, "")
        self.a_list = QtWidgets.QWidget()
        self.a_list.setObjectName("a_list")
        self.a_l_showpub = QtWidgets.QPushButton(self.a_list)
        self.a_l_showpub.setGeometry(QtCore.QRect(1, 3, 341, 231))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_l_showpub.setFont(font)
        self.a_l_showpub.setObjectName("a_l_showpub")
        self.a_l_showpriv = QtWidgets.QPushButton(self.a_list)
        self.a_l_showpriv.setGeometry(QtCore.QRect(348, 3, 341, 231))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_l_showpriv.setFont(font)
        self.a_l_showpriv.setObjectName("a_l_showpriv")
        self.a_l_showpriv.raise_()
        self.a_l_showpub.raise_()
        self.asymmetric_tabs.addTab(self.a_list, "")
        self.a_rename = QtWidgets.QWidget()
        self.a_rename.setObjectName("a_rename")
        self.label_2 = QtWidgets.QLabel(self.a_rename)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 671, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.a_rename)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 251, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.a_rename)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 251, 31))
        self.label_4.setObjectName("label_4")
        self.a_r_rename = QtWidgets.QPushButton(self.a_rename)
        self.a_r_rename.setGeometry(QtCore.QRect(0, 120, 691, 111))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_r_rename.setFont(font)
        self.a_r_rename.setObjectName("a_r_rename")
        self.a_r_oldkey = QtWidgets.QComboBox(self.a_rename)
        self.a_r_oldkey.setGeometry(QtCore.QRect(210, 40, 441, 32))
        self.a_r_oldkey.setObjectName("a_r_oldkey")
        self.a_r_update = QtWidgets.QPushButton(self.a_rename)
        self.a_r_update.setGeometry(QtCore.QRect(657, 40, 31, 31))
        self.a_r_update.setObjectName("a_r_update")
        self.a_r_newkey = QtWidgets.QLineEdit(self.a_rename)
        self.a_r_newkey.setGeometry(QtCore.QRect(210, 80, 477, 32))
        self.a_r_newkey.setObjectName("a_r_newkey")
        self.asymmetric_tabs.addTab(self.a_rename, "")
        self.a_delete = QtWidgets.QWidget()
        self.a_delete.setObjectName("a_delete")
        self.label_5 = QtWidgets.QLabel(self.a_delete)
        self.label_5.setGeometry(QtCore.QRect(4, 10, 251, 31))
        self.label_5.setObjectName("label_5")
        self.a_d_pubdel = QtWidgets.QPushButton(self.a_delete)
        self.a_d_pubdel.setGeometry(QtCore.QRect(3, 50, 341, 181))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_d_pubdel.setFont(font)
        self.a_d_pubdel.setObjectName("a_d_pubdel")
        self.a_d_privdel = QtWidgets.QPushButton(self.a_delete)
        self.a_d_privdel.setGeometry(QtCore.QRect(350, 50, 341, 181))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_d_privdel.setFont(font)
        self.a_d_privdel.setObjectName("a_d_privdel")
        self.a_d_update = QtWidgets.QPushButton(self.a_delete)
        self.a_d_update.setGeometry(QtCore.QRect(656, 10, 31, 31))
        self.a_d_update.setObjectName("a_d_update")
        self.a_d_keyname = QtWidgets.QComboBox(self.a_delete)
        self.a_d_keyname.setGeometry(QtCore.QRect(249, 10, 401, 32))
        self.a_d_keyname.setObjectName("a_d_keyname")
        self.asymmetric_tabs.addTab(self.a_delete, "")
        self.a_import = QtWidgets.QWidget()
        self.a_import.setObjectName("a_import")
        self.a_i_imppub = QtWidgets.QPushButton(self.a_import)
        self.a_i_imppub.setGeometry(QtCore.QRect(3, 50, 341, 181))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_i_imppub.setFont(font)
        self.a_i_imppub.setObjectName("a_i_imppub")
        self.a_i_imppriv = QtWidgets.QPushButton(self.a_import)
        self.a_i_imppriv.setGeometry(QtCore.QRect(350, 50, 341, 181))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_i_imppriv.setFont(font)
        self.a_i_imppriv.setObjectName("a_i_imppriv")
        self.a_i_keyname = QtWidgets.QLineEdit(self.a_import)
        self.a_i_keyname.setGeometry(QtCore.QRect(253, 10, 401, 32))
        self.a_i_keyname.setObjectName("a_i_keyname")
        self.a_i_dialog = QtWidgets.QPushButton(self.a_import)
        self.a_i_dialog.setGeometry(QtCore.QRect(660, 10, 31, 31))
        self.a_i_dialog.setObjectName("a_i_dialog")
        self.label_8 = QtWidgets.QLabel(self.a_import)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 231, 31))
        self.label_8.setObjectName("label_8")
        self.asymmetric_tabs.addTab(self.a_import, "")
        self.a_export = QtWidgets.QWidget()
        self.a_export.setObjectName("a_export")
        self.a_e_keyname = QtWidgets.QComboBox(self.a_export)
        self.a_e_keyname.setGeometry(QtCore.QRect(252, 10, 401, 32))
        self.a_e_keyname.setObjectName("a_e_keyname")
        self.a_e_update = QtWidgets.QPushButton(self.a_export)
        self.a_e_update.setGeometry(QtCore.QRect(659, 10, 31, 31))
        self.a_e_update.setObjectName("a_e_update")
        self.label_6 = QtWidgets.QLabel(self.a_export)
        self.label_6.setGeometry(QtCore.QRect(7, 10, 231, 31))
        self.label_6.setObjectName("label_6")
        self.a_e_output = QtWidgets.QLineEdit(self.a_export)
        self.a_e_output.setGeometry(QtCore.QRect(252, 50, 401, 32))
        self.a_e_output.setObjectName("a_e_output")
        self.a_e_dialog = QtWidgets.QPushButton(self.a_export)
        self.a_e_dialog.setGeometry(QtCore.QRect(659, 50, 31, 31))
        self.a_e_dialog.setObjectName("a_e_dialog")
        self.label_7 = QtWidgets.QLabel(self.a_export)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 231, 31))
        self.label_7.setObjectName("label_7")
        self.a_e_exppub = QtWidgets.QPushButton(self.a_export)
        self.a_e_exppub.setGeometry(QtCore.QRect(3, 90, 341, 141))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_e_exppub.setFont(font)
        self.a_e_exppub.setObjectName("a_e_exppub")
        self.a_e_exppriv = QtWidgets.QPushButton(self.a_export)
        self.a_e_exppriv.setGeometry(QtCore.QRect(350, 90, 341, 141))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_e_exppriv.setFont(font)
        self.a_e_exppriv.setObjectName("a_e_exppriv")
        self.asymmetric_tabs.addTab(self.a_export, "")
        self.a_encrypt = QtWidgets.QWidget()
        self.a_encrypt.setObjectName("a_encrypt")
        self.a_enc_update = QtWidgets.QPushButton(self.a_encrypt)
        self.a_enc_update.setGeometry(QtCore.QRect(657, 10, 31, 31))
        self.a_enc_update.setObjectName("a_enc_update")
        self.a_enc_pubkey = QtWidgets.QComboBox(self.a_encrypt)
        self.a_enc_pubkey.setGeometry(QtCore.QRect(250, 10, 401, 32))
        self.a_enc_pubkey.setObjectName("a_enc_pubkey")
        self.label_9 = QtWidgets.QLabel(self.a_encrypt)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 231, 31))
        self.label_9.setObjectName("label_9")
        self.a_enc_clear = QtWidgets.QLineEdit(self.a_encrypt)
        self.a_enc_clear.setGeometry(QtCore.QRect(250, 49, 401, 32))
        self.a_enc_clear.setObjectName("a_enc_clear")
        self.a_enc_clear_dialog = QtWidgets.QPushButton(self.a_encrypt)
        self.a_enc_clear_dialog.setGeometry(QtCore.QRect(657, 49, 31, 31))
        self.a_enc_clear_dialog.setObjectName("a_enc_clear_dialog")
        self.label_10 = QtWidgets.QLabel(self.a_encrypt)
        self.label_10.setGeometry(QtCore.QRect(10, 50, 231, 31))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.a_encrypt)
        self.label_11.setGeometry(QtCore.QRect(10, 91, 231, 31))
        self.label_11.setObjectName("label_11")
        self.a_enc_crypt_dialog = QtWidgets.QPushButton(self.a_encrypt)
        self.a_enc_crypt_dialog.setGeometry(QtCore.QRect(657, 90, 31, 31))
        self.a_enc_crypt_dialog.setObjectName("a_enc_crypt_dialog")
        self.a_enc_crypt = QtWidgets.QLineEdit(self.a_encrypt)
        self.a_enc_crypt.setGeometry(QtCore.QRect(250, 90, 401, 32))
        self.a_enc_crypt.setObjectName("a_enc_crypt")
        self.a_enc_sign = QtWidgets.QCheckBox(self.a_encrypt)
        self.a_enc_sign.setGeometry(QtCore.QRect(10, 130, 671, 22))
        self.a_enc_sign.setObjectName("a_enc_sign")
        self.a_enc_encrypt = QtWidgets.QPushButton(self.a_encrypt)
        self.a_enc_encrypt.setGeometry(QtCore.QRect(0, 160, 691, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_enc_encrypt.setFont(font)
        self.a_enc_encrypt.setObjectName("a_enc_encrypt")
        self.asymmetric_tabs.addTab(self.a_encrypt, "")
        self.a_decrypt = QtWidgets.QWidget()
        self.a_decrypt.setObjectName("a_decrypt")
        self.label_12 = QtWidgets.QLabel(self.a_decrypt)
        self.label_12.setGeometry(QtCore.QRect(13, 10, 231, 31))
        self.label_12.setObjectName("label_12")
        self.a_dec_decrypt = QtWidgets.QPushButton(self.a_decrypt)
        self.a_dec_decrypt.setGeometry(QtCore.QRect(3, 160, 691, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a_dec_decrypt.setFont(font)
        self.a_dec_decrypt.setObjectName("a_dec_decrypt")
        self.a_dec_privkey = QtWidgets.QComboBox(self.a_decrypt)
        self.a_dec_privkey.setGeometry(QtCore.QRect(253, 10, 401, 32))
        self.a_dec_privkey.setObjectName("a_dec_privkey")
        self.a_dec_verify = QtWidgets.QCheckBox(self.a_decrypt)
        self.a_dec_verify.setGeometry(QtCore.QRect(13, 130, 671, 22))
        self.a_dec_verify.setObjectName("a_dec_verify")
        self.label_13 = QtWidgets.QLabel(self.a_decrypt)
        self.label_13.setGeometry(QtCore.QRect(13, 50, 231, 31))
        self.label_13.setObjectName("label_13")
        self.a_dec_crypt_dialog = QtWidgets.QPushButton(self.a_decrypt)
        self.a_dec_crypt_dialog.setGeometry(QtCore.QRect(660, 49, 31, 31))
        self.a_dec_crypt_dialog.setObjectName("a_dec_crypt_dialog")
        self.a_dec_update = QtWidgets.QPushButton(self.a_decrypt)
        self.a_dec_update.setGeometry(QtCore.QRect(660, 10, 31, 31))
        self.a_dec_update.setObjectName("a_dec_update")
        self.a_dec_clear = QtWidgets.QLineEdit(self.a_decrypt)
        self.a_dec_clear.setGeometry(QtCore.QRect(253, 90, 401, 32))
        self.a_dec_clear.setObjectName("a_dec_clear")
        self.a_dec_crypt = QtWidgets.QLineEdit(self.a_decrypt)
        self.a_dec_crypt.setGeometry(QtCore.QRect(253, 49, 401, 32))
        self.a_dec_crypt.setObjectName("a_dec_crypt")
        self.label_14 = QtWidgets.QLabel(self.a_decrypt)
        self.label_14.setGeometry(QtCore.QRect(13, 91, 231, 31))
        self.label_14.setObjectName("label_14")
        self.a_dec_clear_dialog = QtWidgets.QPushButton(self.a_decrypt)
        self.a_dec_clear_dialog.setGeometry(QtCore.QRect(660, 90, 31, 31))
        self.a_dec_clear_dialog.setObjectName("a_dec_clear_dialog")
        self.asymmetric_tabs.addTab(self.a_decrypt, "")
        self.crypto_mode.addTab(self.asymmetric, "")
        self.symmetric = QtWidgets.QWidget()
        self.symmetric.setObjectName("symmetric")
        self.symmetric_tabs = QtWidgets.QTabWidget(self.symmetric)
        self.symmetric_tabs.setGeometry(QtCore.QRect(2, 10, 701, 261))
        self.symmetric_tabs.setObjectName("symmetric_tabs")
        self.s_generate = QtWidgets.QWidget()
        self.s_generate.setObjectName("s_generate")
        self.s_g_keyname = QtWidgets.QLineEdit(self.s_generate)
        self.s_g_keyname.setGeometry(QtCore.QRect(260, 10, 391, 32))
        self.s_g_keyname.setObjectName("s_g_keyname")
        self.label_15 = QtWidgets.QLabel(self.s_generate)
        self.label_15.setGeometry(QtCore.QRect(10, 11, 231, 31))
        self.label_15.setObjectName("label_15")
        self.s_g_generate = QtWidgets.QPushButton(self.s_generate)
        self.s_g_generate.setGeometry(QtCore.QRect(0, 46, 691, 177))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.s_g_generate.setFont(font)
        self.s_g_generate.setObjectName("s_g_generate")
        self.s_g_dialog = QtWidgets.QPushButton(self.s_generate)
        self.s_g_dialog.setGeometry(QtCore.QRect(655, 11, 31, 31))
        self.s_g_dialog.setObjectName("s_g_dialog")
        self.symmetric_tabs.addTab(self.s_generate, "")
        self.s_encrypt = QtWidgets.QWidget()
        self.s_encrypt.setObjectName("s_encrypt")
        self.s_enc_keyfile_dia = QtWidgets.QPushButton(self.s_encrypt)
        self.s_enc_keyfile_dia.setGeometry(QtCore.QRect(659, 10, 31, 31))
        self.s_enc_keyfile_dia.setObjectName("s_enc_keyfile_dia")
        self.label_16 = QtWidgets.QLabel(self.s_encrypt)
        self.label_16.setGeometry(QtCore.QRect(12, 11, 231, 31))
        self.label_16.setObjectName("label_16")
        self.s_enc_keyfile = QtWidgets.QLineEdit(self.s_encrypt)
        self.s_enc_keyfile.setGeometry(QtCore.QRect(252, 10, 401, 32))
        self.s_enc_keyfile.setObjectName("s_enc_keyfile")
        self.label_17 = QtWidgets.QLabel(self.s_encrypt)
        self.label_17.setGeometry(QtCore.QRect(13, 51, 231, 31))
        self.label_17.setObjectName("label_17")
        self.s_enc_clear = QtWidgets.QLineEdit(self.s_encrypt)
        self.s_enc_clear.setGeometry(QtCore.QRect(253, 50, 401, 32))
        self.s_enc_clear.setObjectName("s_enc_clear")
        self.s_enc_clear_dia = QtWidgets.QPushButton(self.s_encrypt)
        self.s_enc_clear_dia.setGeometry(QtCore.QRect(660, 50, 31, 31))
        self.s_enc_clear_dia.setObjectName("s_enc_clear_dia")
        self.s_enc_crypt = QtWidgets.QLineEdit(self.s_encrypt)
        self.s_enc_crypt.setGeometry(QtCore.QRect(253, 90, 401, 32))
        self.s_enc_crypt.setObjectName("s_enc_crypt")
        self.label_18 = QtWidgets.QLabel(self.s_encrypt)
        self.label_18.setGeometry(QtCore.QRect(13, 91, 231, 31))
        self.label_18.setObjectName("label_18")
        self.s_enc_crypt_dia = QtWidgets.QPushButton(self.s_encrypt)
        self.s_enc_crypt_dia.setGeometry(QtCore.QRect(660, 90, 31, 31))
        self.s_enc_crypt_dia.setObjectName("s_enc_crypt_dia")
        self.s_enc_encrypt = QtWidgets.QPushButton(self.s_encrypt)
        self.s_enc_encrypt.setGeometry(QtCore.QRect(0, 133, 691, 90))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.s_enc_encrypt.setFont(font)
        self.s_enc_encrypt.setObjectName("s_enc_encrypt")
        self.symmetric_tabs.addTab(self.s_encrypt, "")
        self.s_decrypt = QtWidgets.QWidget()
        self.s_decrypt.setObjectName("s_decrypt")
        self.label_19 = QtWidgets.QLabel(self.s_decrypt)
        self.label_19.setGeometry(QtCore.QRect(13, 92, 231, 30))
        self.label_19.setObjectName("label_19")
        self.s_dec_keyfile = QtWidgets.QLineEdit(self.s_decrypt)
        self.s_dec_keyfile.setGeometry(QtCore.QRect(252, 11, 401, 31))
        self.s_dec_keyfile.setObjectName("s_dec_keyfile")
        self.s_dec_crypt_dia = QtWidgets.QPushButton(self.s_decrypt)
        self.s_dec_crypt_dia.setGeometry(QtCore.QRect(660, 51, 31, 30))
        self.s_dec_crypt_dia.setObjectName("s_dec_crypt_dia")
        self.s_dec_clear_dia = QtWidgets.QPushButton(self.s_decrypt)
        self.s_dec_clear_dia.setGeometry(QtCore.QRect(660, 91, 31, 30))
        self.s_dec_clear_dia.setObjectName("s_dec_clear_dia")
        self.s_dec_keyfile_dia = QtWidgets.QPushButton(self.s_decrypt)
        self.s_dec_keyfile_dia.setGeometry(QtCore.QRect(659, 11, 31, 30))
        self.s_dec_keyfile_dia.setObjectName("s_dec_keyfile_dia")
        self.s_dec_clear = QtWidgets.QLineEdit(self.s_decrypt)
        self.s_dec_clear.setGeometry(QtCore.QRect(253, 91, 401, 31))
        self.s_dec_clear.setObjectName("s_dec_clear")
        self.s_dec_crypt = QtWidgets.QLineEdit(self.s_decrypt)
        self.s_dec_crypt.setGeometry(QtCore.QRect(253, 51, 401, 31))
        self.s_dec_crypt.setObjectName("s_dec_crypt")
        self.s_dec_decrypt = QtWidgets.QPushButton(self.s_decrypt)
        self.s_dec_decrypt.setGeometry(QtCore.QRect(0, 134, 691, 89))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.s_dec_decrypt.setFont(font)
        self.s_dec_decrypt.setObjectName("s_dec_decrypt")
        self.label_20 = QtWidgets.QLabel(self.s_decrypt)
        self.label_20.setGeometry(QtCore.QRect(13, 52, 231, 30))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.s_decrypt)
        self.label_21.setGeometry(QtCore.QRect(12, 12, 231, 30))
        self.label_21.setObjectName("label_21")
        self.symmetric_tabs.addTab(self.s_decrypt, "")
        self.s_hash = QtWidgets.QWidget()
        self.s_hash.setObjectName("s_hash")
        self.s_h_hash_dia = QtWidgets.QPushButton(self.s_hash)
        self.s_h_hash_dia.setGeometry(QtCore.QRect(653, 50, 31, 30))
        self.s_h_hash_dia.setObjectName("s_h_hash_dia")
        self.s_h_filename = QtWidgets.QLineEdit(self.s_hash)
        self.s_h_filename.setGeometry(QtCore.QRect(245, 10, 401, 31))
        self.s_h_filename.setObjectName("s_h_filename")
        self.label_22 = QtWidgets.QLabel(self.s_hash)
        self.label_22.setGeometry(QtCore.QRect(6, 51, 231, 30))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.s_hash)
        self.label_23.setGeometry(QtCore.QRect(7, 11, 231, 30))
        self.label_23.setObjectName("label_23")
        self.s_h_hash = QtWidgets.QLineEdit(self.s_hash)
        self.s_h_hash.setGeometry(QtCore.QRect(246, 50, 401, 31))
        self.s_h_hash.setObjectName("s_h_hash")
        self.s_h_filename_dia = QtWidgets.QPushButton(self.s_hash)
        self.s_h_filename_dia.setGeometry(QtCore.QRect(652, 10, 31, 30))
        self.s_h_filename_dia.setObjectName("s_h_filename_dia")
        self.s_h_generate = QtWidgets.QPushButton(self.s_hash)
        self.s_h_generate.setGeometry(QtCore.QRect(0, 93, 691, 131))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.s_h_generate.setFont(font)
        self.s_h_generate.setObjectName("s_h_generate")
        self.symmetric_tabs.addTab(self.s_hash, "")
        self.s_verify = QtWidgets.QWidget()
        self.s_verify.setObjectName("s_verify")
        self.label_24 = QtWidgets.QLabel(self.s_verify)
        self.label_24.setGeometry(QtCore.QRect(5, 51, 231, 30))
        self.label_24.setObjectName("label_24")
        self.s_v_filename_dia = QtWidgets.QPushButton(self.s_verify)
        self.s_v_filename_dia.setGeometry(QtCore.QRect(651, 10, 31, 30))
        self.s_v_filename_dia.setObjectName("s_v_filename_dia")
        self.label_25 = QtWidgets.QLabel(self.s_verify)
        self.label_25.setGeometry(QtCore.QRect(6, 11, 231, 30))
        self.label_25.setObjectName("label_25")
        self.s_v_verify = QtWidgets.QPushButton(self.s_verify)
        self.s_v_verify.setGeometry(QtCore.QRect(-1, 93, 691, 131))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.s_v_verify.setFont(font)
        self.s_v_verify.setObjectName("s_v_verify")
        self.s_v_hash = QtWidgets.QLineEdit(self.s_verify)
        self.s_v_hash.setGeometry(QtCore.QRect(245, 50, 401, 31))
        self.s_v_hash.setObjectName("s_v_hash")
        self.s_v_filename = QtWidgets.QLineEdit(self.s_verify)
        self.s_v_filename.setGeometry(QtCore.QRect(244, 10, 401, 31))
        self.s_v_filename.setObjectName("s_v_filename")
        self.s_v_hash_dia = QtWidgets.QPushButton(self.s_verify)
        self.s_v_hash_dia.setGeometry(QtCore.QRect(652, 50, 31, 30))
        self.s_v_hash_dia.setObjectName("s_v_hash_dia")
        self.symmetric_tabs.addTab(self.s_verify, "")
        self.crypto_mode.addTab(self.symmetric, "")
        self.clear_console = QtWidgets.QPushButton(self.MainWidget)
        self.clear_console.setGeometry(QtCore.QRect(657, 336, 51, 161))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.clear_console.setFont(font)
        self.clear_console.setObjectName("clear_console")
        self.console = QtWidgets.QTextBrowser(self.MainWidget)
        self.console.setGeometry(QtCore.QRect(3, 337, 651, 161))
        self.console.setObjectName("console")
        MainWindow.setCentralWidget(self.MainWidget)

        self.retranslateUi(MainWindow)
        self.crypto_mode.setCurrentIndex(0)
        self.asymmetric_tabs.setCurrentIndex(0)
        self.symmetric_tabs.setCurrentIndex(0)
        self.a_g_generate.clicked.connect(a_generate_keys)
        self.a_l_showpub.clicked.connect(a_show_public)
        self.a_l_showpriv.clicked.connect(a_show_private)
        self.a_r_rename.clicked.connect(a_rename)
        self.a_r_update.clicked.connect(a_rename_update)
        self.a_d_pubdel.clicked.connect(a_delete_pub)
        self.a_d_privdel.clicked.connect(a_delete_priv)
        self.a_d_update.clicked.connect(a_delete_update)
        self.a_i_imppub.clicked.connect(a_import_pub)
        self.a_i_imppriv.clicked.connect(a_import_priv)
        self.a_i_dialog.clicked.connect(a_import_dia)
        self.a_e_exppub.clicked.connect(a_export_pub)
        self.a_e_exppriv.clicked.connect(a_export_priv)
        self.a_e_update.clicked.connect(a_export_update)
        self.a_e_dialog.clicked.connect(a_export_dia)
        self.a_enc_encrypt.clicked.connect(a_encrypt)
        self.a_enc_crypt_dialog.clicked.connect(a_encrypt_out_dia)
        self.a_enc_clear_dialog.clicked.connect(a_encrypt_in_dia)
        self.a_enc_update.clicked.connect(a_encrypt_update)
        self.clear_console.clicked.connect(self.console.clear)
        self.a_dec_update.clicked.connect(a_decrypt_update)
        self.a_dec_crypt_dialog.clicked.connect(a_decrypt_in_dia)
        self.a_dec_clear_dialog.clicked.connect(a_decrypt_out_dia)
        self.a_dec_decrypt.clicked.connect(a_decrypt)
        self.s_g_generate.clicked.connect(s_generate)
        self.s_g_dialog.clicked.connect(s_generate_dia)
        self.s_enc_encrypt.clicked.connect(s_encrypt)
        self.s_enc_crypt_dia.clicked.connect(s_enc_out_dia)
        self.s_enc_clear_dia.clicked.connect(s_enc_in_dia)
        self.s_enc_keyfile_dia.clicked.connect(s_enc_key_dia)
        self.s_dec_decrypt.clicked.connect(s_decrypt)
        self.s_dec_keyfile_dia.clicked.connect(s_dec_key_dia)
        self.s_dec_crypt_dia.clicked.connect(s_dec_in_dia)
        self.s_dec_clear_dia.clicked.connect(s_dec_out_dia)
        self.s_h_generate.clicked.connect(s_hash_generate)
        self.s_h_hash_dia.clicked.connect(s_hash_out_dia)
        self.s_h_filename_dia.clicked.connect(s_hash_in_dia)
        self.s_v_verify.clicked.connect(s_hash_verify)
        self.s_v_hash_dia.clicked.connect(s_ver_out_dia)
        self.s_v_filename_dia.clicked.connect(s_ver_in_dia)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "xCrypt"))
        self.label.setText(_translate("MainWindow", "Name of Keypair (e.g E-Mail Address):"))
        self.a_g_signing.setText(_translate("MainWindow", "Generate Signing Keys (takes a few minutes to generate)"))
        self.a_g_generate.setText(_translate("MainWindow", "Generate Keypair(s)"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_generate), _translate("MainWindow", "Generate"))
        self.a_l_showpub.setText(_translate("MainWindow", "Show Public Keys"))
        self.a_l_showpriv.setText(_translate("MainWindow", "Show Private Keys"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_list), _translate("MainWindow", "List"))
        self.label_2.setText(_translate("MainWindow", "Warning. you can only rename public keys you imported from others!"))
        self.label_3.setText(_translate("MainWindow", "Old Public Key Name:"))
        self.label_4.setText(_translate("MainWindow", "New Public Key Name:"))
        self.a_r_rename.setText(_translate("MainWindow", "Rename Public Key"))
        self.a_r_update.setText(_translate("MainWindow", "U"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_rename), _translate("MainWindow", "Rename"))
        self.label_5.setText(_translate("MainWindow", "Name of Keypair or Public Key:"))
        self.a_d_pubdel.setText(_translate("MainWindow", "Delete Public Key (from other people)"))
        self.a_d_privdel.setText(_translate("MainWindow", "Delete Private Key Pair"))
        self.a_d_update.setText(_translate("MainWindow", "U"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_delete), _translate("MainWindow", "Delete"))
        self.a_i_imppub.setText(_translate("MainWindow", "Import Public Key"))
        self.a_i_imppriv.setText(_translate("MainWindow", "Import Private Key"))
        self.a_i_dialog.setText(_translate("MainWindow", "..."))
        self.label_8.setText(_translate("MainWindow", "Filename of Public or Private Key:"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_import), _translate("MainWindow", "Import"))
        self.a_e_update.setText(_translate("MainWindow", "U"))
        self.label_6.setText(_translate("MainWindow", "Key Name:"))
        self.a_e_dialog.setText(_translate("MainWindow", "..."))
        self.label_7.setText(_translate("MainWindow", "Output Filename:"))
        self.a_e_exppub.setText(_translate("MainWindow", "Export Public Key"))
        self.a_e_exppriv.setText(_translate("MainWindow", "Export Private Key"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_export), _translate("MainWindow", "Export"))
        self.a_enc_update.setText(_translate("MainWindow", "U"))
        self.label_9.setText(_translate("MainWindow", "Public Key Name:"))
        self.a_enc_clear_dialog.setText(_translate("MainWindow", "..."))
        self.label_10.setText(_translate("MainWindow", "Cleartext Input Filename:"))
        self.label_11.setText(_translate("MainWindow", "Encrypted Output Filename:"))
        self.a_enc_crypt_dialog.setText(_translate("MainWindow", "..."))
        self.a_enc_sign.setText(_translate("MainWindow", "Sign the Encrypted File (Signing Keys needed)"))
        self.a_enc_encrypt.setText(_translate("MainWindow", "Encrypt / Sign"))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_encrypt), _translate("MainWindow", "Encrypt/Sign"))
        self.label_12.setText(_translate("MainWindow", "Private Key Name:"))
        self.a_dec_decrypt.setText(_translate("MainWindow", "Decrypt / Verify"))
        self.a_dec_verify.setText(_translate("MainWindow", "Verify the Encrypted File (Signing Keys needed, File needs to be Signed)"))
        self.label_13.setText(_translate("MainWindow", "Encrypted Input Filename:"))
        self.a_dec_crypt_dialog.setText(_translate("MainWindow", "..."))
        self.a_dec_update.setText(_translate("MainWindow", "U"))
        self.label_14.setText(_translate("MainWindow", "Cleartext Output Filename:"))
        self.a_dec_clear_dialog.setText(_translate("MainWindow", "..."))
        self.asymmetric_tabs.setTabText(self.asymmetric_tabs.indexOf(self.a_decrypt), _translate("MainWindow", "Decrypt/Verify"))
        self.crypto_mode.setTabText(self.crypto_mode.indexOf(self.asymmetric), _translate("MainWindow", "Asymmetric Encryption"))
        self.label_15.setText(_translate("MainWindow", "Key Output File:"))
        self.s_g_generate.setText(_translate("MainWindow", "Generate Key"))
        self.s_g_dialog.setText(_translate("MainWindow", "..."))
        self.symmetric_tabs.setTabText(self.symmetric_tabs.indexOf(self.s_generate), _translate("MainWindow", "Generate"))
        self.s_enc_keyfile_dia.setText(_translate("MainWindow", "..."))
        self.label_16.setText(_translate("MainWindow", "Key Filename:"))
        self.label_17.setText(_translate("MainWindow", "Cleartext Input Filename:"))
        self.s_enc_clear_dia.setText(_translate("MainWindow", "..."))
        self.label_18.setText(_translate("MainWindow", "Encrypted Output Filename:"))
        self.s_enc_crypt_dia.setText(_translate("MainWindow", "..."))
        self.s_enc_encrypt.setText(_translate("MainWindow", "Encrypt"))
        self.symmetric_tabs.setTabText(self.symmetric_tabs.indexOf(self.s_encrypt), _translate("MainWindow", "Encrypt"))
        self.label_19.setText(_translate("MainWindow", "Cleartext Output Filename:"))
        self.s_dec_crypt_dia.setText(_translate("MainWindow", "..."))
        self.s_dec_clear_dia.setText(_translate("MainWindow", "..."))
        self.s_dec_keyfile_dia.setText(_translate("MainWindow", "..."))
        self.s_dec_decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.label_20.setText(_translate("MainWindow", "Encrypted Input Filename:"))
        self.label_21.setText(_translate("MainWindow", "Key Filename:"))
        self.symmetric_tabs.setTabText(self.symmetric_tabs.indexOf(self.s_decrypt), _translate("MainWindow", "Decrypt"))
        self.s_h_hash_dia.setText(_translate("MainWindow", "..."))
        self.label_22.setText(_translate("MainWindow", "Hash Filename:"))
        self.label_23.setText(_translate("MainWindow", "Filename:"))
        self.s_h_filename_dia.setText(_translate("MainWindow", "..."))
        self.s_h_generate.setText(_translate("MainWindow", "Generate Hashes"))
        self.symmetric_tabs.setTabText(self.symmetric_tabs.indexOf(self.s_hash), _translate("MainWindow", "Generate Hash"))
        self.label_24.setText(_translate("MainWindow", "Hash Filename:"))
        self.s_v_filename_dia.setText(_translate("MainWindow", "..."))
        self.label_25.setText(_translate("MainWindow", "Filename:"))
        self.s_v_verify.setText(_translate("MainWindow", "Verify Hashes"))
        self.s_v_hash_dia.setText(_translate("MainWindow", "..."))
        self.symmetric_tabs.setTabText(self.symmetric_tabs.indexOf(self.s_verify), _translate("MainWindow", "Verify Hash"))
        self.crypto_mode.setTabText(self.crypto_mode.indexOf(self.symmetric), _translate("MainWindow", "Symmetric Encryption"))
        self.clear_console.setText(_translate("MainWindow", "Clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
