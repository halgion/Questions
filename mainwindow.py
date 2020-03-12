# -*- coding: utf-8 -*-

'''
    主界面
'''

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import database as mydb
from AddSingleChoiceWindow import *
from AddMultipleChoiceWindow import *
from AddToFWindow import *
from AddFillinBlanksWindow import *
from AddCalculationWindow import *
from AddProofWindow import *
from SelectSectionsWindow import *
import myfunctions as myfun

class MainWindow(QWidget):
	singal_sectionid = pyqtSignal(list)

	def __init__(self, parent=None):
		super(MainWindow , self).__init__(parent)
		self.ver = '2020.03.11'
		self.selected_sectionids_in_ExportBox = [48, 49, 50, 51, 52, 53]
		self.last_added_section_id = 1
		self.last_added_difficulty_id = 1
		self.last_added_source_id = 1
		self.retrieve_data()
		
		mainlayout = QVBoxLayout()

		self.createDBDisplayBox()
		mainlayout.addWidget(self.DBDisplayBox)

		self.tabs = QTabWidget()
		self.tab_information = QWidget()
		self.tab_modification = QWidget()
		self.tab_export_by_section = QWidget()
		self.tab_export_by_question = QWidget()
		self.tabs.addTab(self.tab_information, '题库概览')
		self.tabs.addTab(self.tab_modification, '录入与修改题目')
		self.tabs.addTab(self.tab_export_by_section, '按章节导出')
		self.tabs.addTab(self.tab_export_by_question, '自由选题导出')
		self.tab_informationUI()
		self.tab_modificationUI()
		self.tab_exportUI()
		mainlayout.addWidget(self.tabs)

		layout_about = QHBoxLayout()
		self.download_demo = QLabel(
			'<a href = "http://www.jhanmath.com/?page_id=125">'
			'下载视频演示</a>')
		self.download_demo.setOpenExternalLinks(True)
		self.download_demo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		layout_about.addWidget(self.download_demo)
		self.about = QLabel(
			'This software is developed by Jing Han. ver %s.' % (self.ver))
		self.about.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout_about.addWidget(self.about)
		mainlayout.addLayout(layout_about)

		self.setLayout(mainlayout)

		self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)

		self.resize(1000, 800)
		self.setWindowTitle("数学题库")

	def tab_informationUI(self):
		layout = QVBoxLayout()
		self.createTotalQuestionsNumBox()
		layout.addWidget(self.TotalQuestionsNumBox)
		self.createBrowseBox()
		layout.addWidget(self.BrowseBox)
		layout.setStretchFactor(self.TotalQuestionsNumBox, 1)
		layout.setStretchFactor(self.BrowseBox, 100)
		self.tab_information.setLayout(layout)		

	def tab_modificationUI(self):
		layout = QVBoxLayout()
		self.createAddQuestionBox()
		layout.addWidget(self.AddQuestionBox)
		self.createModifyQuestionBox()
		layout.addWidget(self.ModifyQuestionBox)
		self.tab_modification.setLayout(layout)

	def tab_exportUI(self):
		layout = QVBoxLayout()
		self.createSectionsBox()
		layout.addWidget(self.SectionsBox)
		self.createExportBox()
		layout.addWidget(self.ExportBox)
		self.tab_export_by_section.setLayout(layout)

	def createDBDisplayBox(self):
		self.DBDisplayBox = QGroupBox('当前题库')
		layout = QHBoxLayout()
		searchstring = 'select name from dbname'
		self.dbname = mydb.search(searchstring)[0][0]
		self.lbl_dbname = QLabel('当前数据库: ' + self.dbname)
		self.btn_dbname = QPushButton('更换题库')
		fm = QFontMetrics(self.btn_dbname.font())
		self.btn_dbname.setFixedWidth(fm.width(self.btn_dbname.text())+20)
		layout.addWidget(self.lbl_dbname)
		layout.addWidget(self.btn_dbname)
		self.DBDisplayBox.setLayout(layout)

	def createTotalQuestionsNumBox(self):
		self.TotalQuestionsNumBox = QGroupBox('各类型题目总数')
		layout = QVBoxLayout()
		self.tbl_total_questions_num = QTableWidget()
		self.tbl_total_questions_num.setRowCount(1)
		self.tbl_total_questions_num.setColumnCount(6)
		self.tbl_total_questions_num.verticalHeader().setVisible(False)
		self.tbl_total_questions_num.setHorizontalHeaderLabels(['单选题数','多选题数','判断题数','填空题数','计算题数','证明题数'])
		self.tbl_total_questions_num.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.tbl_total_questions_num.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tbl_total_questions_num.setSelectionMode(QAbstractItemView.NoSelection)
		self.update_total_questions_sum()
		self.tbl_total_questions_num.setFixedHeight(80)
		self.tbl_total_questions_num.setStyleSheet('''QTableWidget { border: 0; }''')
		self.tbl_total_questions_num.setGridStyle(0)
		layout.addWidget(self.tbl_total_questions_num)
		self.TotalQuestionsNumBox.setLayout(layout)
		self.TotalQuestionsNumBox.setMaximumHeight(self.tbl_total_questions_num.width()+20)
		
	def createBrowseBox(self):
		self.chapters_selected_previously = []
		self.selected_sectionsid_in_BrowseBox = []

		self.BrowseBox = QGroupBox('浏览题目')
		layout = QGridLayout()
		self.tree_sections = QTreeWidget()
		self.tree_sections.setColumnCount(1)
		self.tree_sections.setMaximumWidth(500)
		self.tree_sections.setSelectionMode(QAbstractItemView.MultiSelection)
		self.tree_sections.setHeaderLabels(['选择章节(可多选)'])
		self.roots_in_BrowseBox = []
		for i in range(len(self.chapters)):
			root = QTreeWidgetItem(self.tree_sections)
			root.setText(0, self.chapters[i][1])
			secs_in_this_chp = []
			j = 0
			for j in range(len(self.sections)):
				if self.sections[j][2] == self.chapters[i][0]:
					secs_in_this_chp.append(self.sections[j][1])
			for j in range(len(secs_in_this_chp)):
				child = QTreeWidgetItem(root)
				child.setText(0, secs_in_this_chp[j])
			self.roots_in_BrowseBox.append(root)
			self.tree_sections.addTopLevelItem(root)
		self.tree_sections.clicked.connect(self.tree_sections_clicked)
		layout.addWidget(self.tree_sections, 0, 0, 2, 1)

		layout2 = QGridLayout()
		self.chk_schoice_in_BrowseBox = QCheckBox('单选题')
		self.chk_mchoice_in_BrowseBox = QCheckBox('多选题')
		self.chk_tof_in_BrowseBox = QCheckBox('判断题')
		self.chk_blank_in_BrowseBox = QCheckBox('填空题')
		self.chk_calculation_in_BrowseBox = QCheckBox('计算题')
		self.chk_proof_in_BrowseBox = QCheckBox('证明题')
		self.chk_schoice_in_BrowseBox.setChecked(True)
		self.chk_mchoice_in_BrowseBox.setChecked(True)
		self.chk_tof_in_BrowseBox.setChecked(True)
		self.chk_blank_in_BrowseBox.setChecked(True)
		self.chk_calculation_in_BrowseBox.setChecked(True)
		self.chk_proof_in_BrowseBox.setChecked(True)
		self.chk_schoice_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_mchoice_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_tof_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_blank_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_calculation_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		self.chk_proof_in_BrowseBox.clicked.connect(self.update_preview_in_BrowseBox)
		layout2.addWidget(self.chk_schoice_in_BrowseBox, 0, 0)
		layout2.addWidget(self.chk_mchoice_in_BrowseBox, 0, 1)
		layout2.addWidget(self.chk_tof_in_BrowseBox, 0, 2)
		layout2.addWidget(self.chk_blank_in_BrowseBox, 1, 0)
		layout2.addWidget(self.chk_calculation_in_BrowseBox, 1, 1)
		layout2.addWidget(self.chk_proof_in_BrowseBox, 1, 2)
		layout.addLayout(layout2, 0, 1)

		self.webView_in_BrowseBox = QWebEngineView()
		self.webView_in_BrowseBox.setMinimumSize(600, 400)
		self.webView_in_BrowseBox.setContextMenuPolicy(0) # 禁止右键菜单
		self.update_preview_in_BrowseBox()
		layout.addWidget(self.webView_in_BrowseBox, 1, 1)
		layout.setHorizontalSpacing(20)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 3)
		self.BrowseBox.setLayout(layout)

	def createAddQuestionBox(self):
		self.AddQuestionBox = QGroupBox("添加题目")
		layout = QHBoxLayout()
		self.btn_addschoice = QPushButton('添加单选题')
		self.btn_addschoice.clicked.connect(self.btn_addschoice_clicked)
		self.btn_addmchoice = QPushButton('添加多选题')
		self.btn_addmchoice.clicked.connect(self.btn_addmchoice_clicked)
		self.btn_addtof = QPushButton('添加判断题')
		self.btn_addtof.clicked.connect(self.btn_addtof_clicked)
		self.btn_addblank = QPushButton('添加填空题')
		self.btn_addblank.clicked.connect(self.btn_addblank_clicked)
		self.btn_addcalculate = QPushButton('添加计算题')
		self.btn_addcalculate.clicked.connect(self.btn_addcalculate_clicked)
		self.btn_addprove = QPushButton('添加证明题')
		self.btn_addprove.clicked.connect(self.btn_addprove_clicked)
		layout.setSpacing(10)
		layout.addWidget(self.btn_addschoice)
		layout.addWidget(self.btn_addmchoice)
		layout.addWidget(self.btn_addtof)
		layout.addWidget(self.btn_addblank)
		layout.addWidget(self.btn_addcalculate)
		layout.addWidget(self.btn_addprove)
		self.AddQuestionBox.setLayout(layout)

	def createModifyQuestionBox(self):
		self.ModifyQuestionBox = QGroupBox('修改题目')
		self.sectionid_selected_in_ModifyBox = 0 # 当前选择的章节id，0表示未选择
		self.questionid_in_ModifyBox = 0 # 当前显示的问题的id，0表示未选择
		self.questionids_in_ModifyBox = [] # 当前显示的章节下符合条件的全部问题的id
		self.question_data_in_ModifyBox = [] # 当前显示的问题的详细数据

		layout = QGridLayout()
		self.tree_sections_in_ModifyBox = QTreeWidget()
		self.tree_sections_in_ModifyBox.setColumnCount(1)
		self.tree_sections_in_ModifyBox.setMaximumWidth(500)
		self.tree_sections_in_ModifyBox.setSelectionMode(QAbstractItemView.SingleSelection)
		self.tree_sections_in_ModifyBox.setHeaderLabels(['选择节(单选子节点)'])
		self.roots_in_ModifyBox = []
		for i in range(len(self.chapters)):
			root = QTreeWidgetItem(self.tree_sections_in_ModifyBox)
			root.setText(0, self.chapters[i][1])
			secs_in_this_chp = []
			j = 0
			for j in range(len(self.sections)):
				if self.sections[j][2] == self.chapters[i][0]:
					secs_in_this_chp.append(self.sections[j][1])
			for j in range(len(secs_in_this_chp)):
				child = QTreeWidgetItem(root)
				child.setText(0, secs_in_this_chp[j])
			self.roots_in_ModifyBox.append(root)
			self.tree_sections_in_ModifyBox.addTopLevelItem(root)
		layout.addWidget(self.tree_sections_in_ModifyBox, 0, 0, 3, 1)

		layout2 = QHBoxLayout()
		self.list_type_of_question_in_ModifyBox = QComboBox()
		self.list_type_of_question_in_ModifyBox.addItems(['单选题','多选题','判断题','填空题','计算题','证明题'])
		self.list_type_of_question_in_ModifyBox.setCurrentIndex(0)
		self.list_type_of_question_in_ModifyBox.currentIndexChanged.connect(self.retrieve_questionids_in_ModifyBox)
		self.lbl_sequence_in_ModifyBox = QLabel('题目序列：0/0')
		self.lbl_sequence_in_ModifyBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		layout2.addWidget(self.list_type_of_question_in_ModifyBox)
		layout2.addWidget(self.lbl_sequence_in_ModifyBox)
		layout.addLayout(layout2, 0, 1, 1, 3)

		self.webView_in_ModifyBox = QWebEngineView()
		self.webView_in_ModifyBox.setMinimumSize(600, 400)
		self.webView_in_ModifyBox.setContextMenuPolicy(0) # 禁止右键菜单
		layout.addWidget(self.webView_in_ModifyBox, 1, 1, 1, 3)

		layout_navi_btn = QHBoxLayout()
		self.btn_previous = QPushButton('上一题(&Z)')
		self.btn_next = QPushButton('下一题(&X)')
		self.btn_modify = QPushButton('修改(&M)')
		self.btn_copy = QPushButton('复制(&C)')
		self.btn_delete = QPushButton('删除(&D)')
		fm = QFontMetrics(self.btn_modify.font())
		margin = 4
		self.btn_previous.setFixedWidth(fm.width(self.btn_previous.text()) + margin)
		self.btn_next.setFixedWidth(fm.width(self.btn_next.text()) + margin)
		self.btn_modify.setFixedWidth(fm.width(self.btn_modify.text()) + margin)
		self.btn_copy.setFixedWidth(fm.width(self.btn_copy.text()) + margin)
		self.btn_delete.setFixedWidth(fm.width(self.btn_delete.text()) + margin)
		self.btn_previous.setEnabled(False)
		self.btn_modify.setEnabled(False)
		self.btn_next.setEnabled(False)
		self.btn_delete.setEnabled(False)
		self.btn_copy.setEnabled(False)
		self.btn_previous.clicked.connect(self.btn_previous_clicked)
		self.btn_next.clicked.connect(self.btn_next_clicked)
		self.btn_modify.clicked.connect(self.btn_modify_clicked)
		self.btn_delete.clicked.connect(self.btn_delete_clicked)
		self.btn_copy.clicked.connect(self.btn_copy_clicked)
		layout_navi_btn.addWidget(self.btn_previous)
		layout_navi_btn.addWidget(self.btn_modify)
		layout_navi_btn.addWidget(self.btn_copy)
		layout_navi_btn.addWidget(self.btn_delete)
		layout_navi_btn.addWidget(self.btn_next)

		self.update_preview_in_ModifyBox()
		self.tree_sections_in_ModifyBox.clicked.connect(self.tree_sections_in_ModifyBox_clicked)
		
		layout.addLayout(layout_navi_btn,2,2)
		layout.setHorizontalSpacing(20)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 100)
		self.ModifyQuestionBox.setLayout(layout)		

	def createSectionsBox(self):
		self.SectionsBox = QGroupBox('选择导出章节')
		layout = QVBoxLayout()
		self.tbl_selectedsections = QTableWidget()
		self.tbl_selectedsections.setColumnCount(7)
		self.tbl_selectedsections.setHorizontalHeaderLabels(['章节','单选题数','多选题数','判断题数','填空题数','计算题数','证明题数'])
		self.tbl_selectedsections.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.tbl_selectedsections.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tbl_selectedsections.setSelectionBehavior(QAbstractItemView.SelectRows)
		layout.addWidget(self.tbl_selectedsections)
		self.btn_changesections = QPushButton('选择章节')
		self.btn_changesections.clicked.connect(self.btn_changesections_clicked)
		layout.addWidget(self.btn_changesections)
		self.SectionsBox.setLayout(layout)

	def createExportBox(self):
		self.lbl_schoice = QLabel('单选题数量：')
		self.lbl_mchoice = QLabel('多选题数量：')
		self.lbl_tof = QLabel('判断题数量：')
		self.lbl_blank = QLabel('填空题数量：')
		self.lbl_calculate = QLabel('计算题数量：')
		self.lbl_prove = QLabel('证明题数量:')
		self.ed_schoice = QLineEdit('0')
		self.ed_mchoice = QLineEdit('0')
		self.ed_tof = QLineEdit('0')
		self.ed_blank = QLineEdit('0')
		self.ed_calculate = QLineEdit('0')
		self.ed_prove = QLineEdit('0')
		regex = QRegExp("^[1-9]\d*|0$")
		validator = QRegExpValidator(regex)
		self.ed_schoice.setValidator(validator)
		self.ed_mchoice.setValidator(validator)
		self.ed_tof.setValidator(validator)
		self.ed_blank.setValidator(validator)
		self.ed_calculate.setValidator(validator)
		self.ed_prove.setValidator(validator)
		self.ed_schoice.setAlignment(Qt.AlignRight)
		self.ed_mchoice.setAlignment(Qt.AlignRight)
		self.ed_tof.setAlignment(Qt.AlignRight)
		self.ed_blank.setAlignment(Qt.AlignRight)
		self.ed_calculate.setAlignment(Qt.AlignRight)
		self.ed_prove.setAlignment(Qt.AlignRight)
		self.ed_schoice.setFixedWidth(100)
		self.ed_mchoice.setFixedWidth(100)
		self.ed_tof.setFixedWidth(100)
		self.ed_blank.setFixedWidth(100)
		self.ed_calculate.setFixedWidth(100)
		self.ed_prove.setFixedWidth(100)
		self.chk_solution = QCheckBox('包含解答')
		self.chk_random = QCheckBox('打乱题目顺序')
		self.chk_randomchoice = QCheckBox('选择题选项乱序')
		self.chk_white = QCheckBox('主观题后留空')
		self.chk_follow = QCheckBox('解答跟随小题')
		self.chk_distribute = QCheckBox('平均分配各节题目数量')
		self.chk_easy = QCheckBox('简单')
		self.chk_medium = QCheckBox('中等')
		self.chk_hard = QCheckBox('困难')
		self.chk_hell = QCheckBox('地狱')
		self.btn_export = QPushButton('导出')
		self.btn_export.clicked.connect(self.export_questions)
		self.btn_compile = QPushButton('导出并编译')
		self.btn_compile.setEnabled(False)

		layout = QGridLayout()
		layout.addWidget(self.lbl_schoice, 0, 0)
		layout.addWidget(self.lbl_mchoice, 1, 0)
		layout.addWidget(self.lbl_tof, 2, 0)
		layout.addWidget(self.lbl_blank, 3, 0)
		layout.addWidget(self.lbl_calculate, 4, 0)
		layout.addWidget(self.lbl_prove, 5, 0)
		layout.addWidget(self.ed_schoice, 0, 1)
		layout.addWidget(self.ed_mchoice, 1, 1)
		layout.addWidget(self.ed_tof, 2, 1)
		layout.addWidget(self.ed_blank, 3, 1)
		layout.addWidget(self.ed_calculate, 4, 1)
		layout.addWidget(self.ed_prove, 5, 1)
		layout.addWidget(self.chk_solution, 0, 3)
		layout.addWidget(self.chk_follow, 1, 3)
		layout.addWidget(self.chk_white, 2, 3)
		layout.addWidget(self.chk_random, 3, 3)
		layout.addWidget(self.chk_randomchoice, 4, 3)
		layout.addWidget(self.chk_distribute, 5, 3)
		layout.addWidget(self.chk_easy, 0, 4)
		layout.addWidget(self.chk_medium, 1, 4)
		layout.addWidget(self.chk_hard, 2, 4)
		layout.addWidget(self.chk_hell, 3, 4)
		layout.addWidget(self.btn_export, 1, 6, 2, 1)
		layout.addWidget(self.btn_compile, 3, 6, 2, 1)
		layout.addWidget(QLabel(' '), 0, 2)
		layout.addWidget(QLabel(' '), 0, 5)
		layout.setHorizontalSpacing(30)

		self.ExportBox = QGroupBox('导出选项')
		self.ExportBox.setLayout(layout)

	def btn_changesections_clicked(self):
		self.select_sections_ui = SelectSections()
		self.select_sections_ui.signal.connect(self.update_sections_in_ExportBox)
		self.singal_sectionid.connect(self.select_sections_ui.initialize)
		self.singal_sectionid.emit(self.selected_sectionids_in_ExportBox)
		self.select_sections_ui.show()

	def btn_addschoice_clicked(self):
		self.add_schoice_ui = AddSingleChoice()
		self.transmit_settings(self.add_schoice_ui)
		self.add_schoice_ui.show()

	def btn_addmchoice_clicked(self):
		self.add_mchoice_ui = AddMultipleChoice()
		self.transmit_settings(self.add_mchoice_ui)
		self.add_mchoice_ui.show()

	def btn_addtof_clicked(self):
		self.add_tof_ui = AddToF()
		self.transmit_settings(self.add_tof_ui)
		self.add_tof_ui.show()
	
	def btn_addblank_clicked(self):
		self.add_blank_ui = AddFillinBlanks()
		self.transmit_settings(self.add_blank_ui)
		self.add_blank_ui.show()

	def btn_addcalculate_clicked(self):
		self.add_calculation_ui = AddCalculation()
		self.transmit_settings(self.add_calculation_ui)
		self.add_calculation_ui.show()

	def btn_addprove_clicked(self):
		self.add_proof_ui = AddProof()
		self.transmit_settings(self.add_proof_ui)
		self.add_proof_ui.show()

	def btn_previous_clicked(self):
		index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
		if index != 0:
			self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index-1]
		self.update_preview_in_ModifyBox()

	def btn_next_clicked(self):
		index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
		if index != len(self.questionids_in_ModifyBox)-1:
			self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index+1]
		self.update_preview_in_ModifyBox()
	
	def btn_modify_clicked(self):
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			self.add_schoice_ui = AddSingleChoice()
			self.add_schoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_schoice_ui.input_answerA.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerB.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerC.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerD.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			if self.question_data_in_ModifyBox[5] == 'A':
				self.add_schoice_ui.btn_A.setChecked(Ture)
				self.add_schoice_ui.clickA()
			elif self.question_data_in_ModifyBox[5] == 'B':
				self.add_schoice_ui.btn_B.setChecked(True)
				self.add_schoice_ui.clickB()
			elif self.question_data_in_ModifyBox[5] == 'C':
				self.add_schoice_ui.btn_C.setChecked(True)
				self.add_schoice_ui.clickC()
			elif self.question_data_in_ModifyBox[5] == 'D':
				self.add_schoice_ui.btn_D.setChecked(True)
				self.add_schoice_ui.clickD()
			self.add_schoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[6]))
			i = 0
			while self.question_data_in_ModifyBox[7] != self.sections[i][0]:
				i += 1
			self.add_schoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.difficulties[i][0]:
				i += 1
			self.add_schoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[9] != self.sources[i][0]:
				i += 1
			self.add_schoice_ui.list_source.setCurrentIndex(i)
			self.add_schoice_ui.other_settings.connect(self.update_after_modification)
			self.add_schoice_ui.modification = self.questionid_in_ModifyBox
			self.add_schoice_ui.btn_add.setText('修改题目')
			# self.add_schoice_ui.update_preview()
			self.add_schoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			self.add_mchoice_ui = AddMultipleChoice()
			self.add_mchoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_mchoice_ui.input_answerA.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerB.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerC.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerD.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			self.add_mchoice_ui.btn_A.setCurrentIndex(self.question_data_in_ModifyBox[5])
			self.add_mchoice_ui.btn_B.setCurrentIndex(self.question_data_in_ModifyBox[6])
			self.add_mchoice_ui.btn_C.setCurrentIndex(self.question_data_in_ModifyBox[7])
			self.add_mchoice_ui.btn_D.setCurrentIndex(self.question_data_in_ModifyBox[8])
			self.add_mchoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[9]))
			i = 0
			while self.question_data_in_ModifyBox[10] != self.sections[i][0]:
				i += 1
			self.add_mchoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[11] != self.difficulties[i][0]:
				i += 1
			self.add_mchoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[12] != self.sources[i][0]:
				i += 1
			self.add_mchoice_ui.list_source.setCurrentIndex(i)
			self.add_mchoice_ui.other_settings.connect(self.update_after_modification)
			self.add_mchoice_ui.modification = self.questionid_in_ModifyBox
			self.add_mchoice_ui.btn_add.setText('修改题目')
			# self.add_mchoice_ui.update_preview()
			self.add_mchoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			self.add_tof_ui = AddToF()
			self.add_tof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_tof_ui.list_answer.setCurrentIndex(self.question_data_in_ModifyBox[1])
			self.add_tof_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			i = 0
			while self.question_data_in_ModifyBox[3] != self.sections[i][0]:
				i += 1
			self.add_tof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.difficulties[i][0]:
				i += 1
			self.add_tof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[5] != self.sources[i][0]:
				i += 1
			self.add_tof_ui.list_source.setCurrentIndex(i)
			self.add_tof_ui.other_settings.connect(self.update_after_modification)
			self.add_tof_ui.modification = self.questionid_in_ModifyBox
			self.add_tof_ui.btn_add.setText('修改题目')
			# self.add_tof_ui.update_preview()
			self.add_tof_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			self.add_blank_ui = AddFillinBlanks()
			self.add_blank_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_blank_ui.input_answer1.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer2.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer3.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer4.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			self.add_blank_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[5]))
			i = 0
			while self.question_data_in_ModifyBox[6] != self.sections[i][0]:
				i += 1
			self.add_blank_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[7] != self.difficulties[i][0]:
				i += 1
			self.add_blank_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.sources[i][0]:
				i += 1
			self.add_blank_ui.list_source.setCurrentIndex(i)
			self.add_blank_ui.other_settings.connect(self.update_after_modification)
			self.add_blank_ui.modification = self.questionid_in_ModifyBox
			self.add_blank_ui.btn_add.setText('修改题目')
			# self.add_blank_ui.update_preview()
			self.add_blank_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			self.add_calculation_ui = AddCalculation()
			self.add_calculation_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_calculation_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_calculation_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_calculation_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_calculation_ui.list_source.setCurrentIndex(i)
			self.add_calculation_ui.other_settings.connect(self.update_after_modification)
			self.add_calculation_ui.modification = self.questionid_in_ModifyBox
			self.add_calculation_ui.btn_add.setText('修改题目')
			# self.add_calculation_ui.update_preview()
			self.add_calculation_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			self.add_proof_ui = AddProof()
			self.add_proof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_proof_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_proof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_proof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_proof_ui.list_source.setCurrentIndex(i)
			self.add_proof_ui.other_settings.connect(self.update_after_modification)
			self.add_proof_ui.modification = self.questionid_in_ModifyBox
			self.add_proof_ui.btn_add.setText('修改题目')
			# self.add_proof_ui.update_preview()
			self.add_proof_ui.show()

	def btn_delete_clicked(self):
		reply = QMessageBox.question(self, u'询问', u'确认删除当前题目？', QMessageBox.Yes, QMessageBox.No)
		if reply == QMessageBox.Yes:
			if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
				deletestring = ('delete from schoice where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
				deletestring = ('delete from mchoice where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
				deletestring = ('delete from tof where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
				deletestring = ('delete from blank where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
				deletestring = ('delete from calculation where id = %d' % (self.questionid_in_ModifyBox))
			if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
				deletestring = ('delete from proof where id = %d' % (self.questionid_in_ModifyBox))
			if mydb.insert(deletestring):
				QMessageBox.about(self, '通知', '删除成功！')
				index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
				self.questionids_in_ModifyBox.remove(self.questionid_in_ModifyBox)
				if len(self.questionids_in_ModifyBox) == 0:
					self.questionid_in_ModifyBox = 0 # 如果删除后当前题目列表为空，则问题id清0
				elif index == len(self.questionids_in_ModifyBox):
					self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index - 1]
				else:
					self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index]
				self.update_preview_in_ModifyBox()
				self.update_preview_in_BrowseBox()
				self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)
			else:
				QMessageBox.about(self, '通知', '删除失败！')

	def btn_copy_clicked(self):
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			self.add_schoice_ui = AddSingleChoice()
			self.add_schoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_schoice_ui.input_answerA.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerB.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerC.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_schoice_ui.input_answerD.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			if self.question_data_in_ModifyBox[5] == 'A':
				self.add_schoice_ui.btn_A.setChecked(Ture)
				self.add_schoice_ui.clickA()
			elif self.question_data_in_ModifyBox[5] == 'B':
				self.add_schoice_ui.btn_B.setChecked(True)
				self.add_schoice_ui.clickB()
			elif self.question_data_in_ModifyBox[5] == 'C':
				self.add_schoice_ui.btn_C.setChecked(True)
				self.add_schoice_ui.clickC()
			elif self.question_data_in_ModifyBox[5] == 'D':
				self.add_schoice_ui.btn_D.setChecked(True)
				self.add_schoice_ui.clickD()
			self.add_schoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[6]))
			i = 0
			while self.question_data_in_ModifyBox[7] != self.sections[i][0]:
				i += 1
			self.add_schoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.difficulties[i][0]:
				i += 1
			self.add_schoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[9] != self.sources[i][0]:
				i += 1
			self.add_schoice_ui.list_source.setCurrentIndex(i)
			self.add_schoice_ui.other_settings.connect(self.update_after_insertion)
			# self.add_schoice_ui.update_preview()
			self.add_schoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			self.add_mchoice_ui = AddMultipleChoice()
			self.add_mchoice_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_mchoice_ui.input_answerA.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerB.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerC.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_mchoice_ui.input_answerD.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			self.add_mchoice_ui.btn_A.setCurrentIndex(self.question_data_in_ModifyBox[5])
			self.add_mchoice_ui.btn_B.setCurrentIndex(self.question_data_in_ModifyBox[6])
			self.add_mchoice_ui.btn_C.setCurrentIndex(self.question_data_in_ModifyBox[7])
			self.add_mchoice_ui.btn_D.setCurrentIndex(self.question_data_in_ModifyBox[8])
			self.add_mchoice_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[9]))
			i = 0
			while self.question_data_in_ModifyBox[10] != self.sections[i][0]:
				i += 1
			self.add_mchoice_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[11] != self.difficulties[i][0]:
				i += 1
			self.add_mchoice_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[12] != self.sources[i][0]:
				i += 1
			self.add_mchoice_ui.list_source.setCurrentIndex(i)
			self.add_mchoice_ui.other_settings.connect(self.update_after_insertion)
			# self.add_mchoice_ui.update_preview()
			self.add_mchoice_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			self.add_tof_ui = AddToF()
			self.add_tof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_tof_ui.list_answer.setCurrentIndex(self.question_data_in_ModifyBox[1])
			self.add_tof_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[2]))
			i = 0
			while self.question_data_in_ModifyBox[3] != self.sections[i][0]:
				i += 1
			self.add_tof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.difficulties[i][0]:
				i += 1
			self.add_tof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[5] != self.sources[i][0]:
				i += 1
			self.add_tof_ui.list_source.setCurrentIndex(i)
			self.add_tof_ui.other_settings.connect(self.update_after_insertion)
			# self.add_tof_ui.update_preview()
			self.add_tof_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			self.add_blank_ui = AddFillinBlanks()
			self.add_blank_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_blank_ui.input_answer1.setPlainText(self.question_data_in_ModifyBox[1].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer2.setPlainText(self.question_data_in_ModifyBox[2].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer3.setPlainText(self.question_data_in_ModifyBox[3].replace('\\\\\n','\n'))
			self.add_blank_ui.input_answer4.setPlainText(self.question_data_in_ModifyBox[4].replace('\\\\\n','\n'))
			self.add_blank_ui.input_explain.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[5]))
			i = 0
			while self.question_data_in_ModifyBox[6] != self.sections[i][0]:
				i += 1
			self.add_blank_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[7] != self.difficulties[i][0]:
				i += 1
			self.add_blank_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[8] != self.sources[i][0]:
				i += 1
			self.add_blank_ui.list_source.setCurrentIndex(i)
			self.add_blank_ui.other_settings.connect(self.update_after_insertion)
			# self.add_blank_ui.update_preview()
			self.add_blank_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			self.add_calculation_ui = AddCalculation()
			self.add_calculation_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_calculation_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_calculation_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_calculation_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_calculation_ui.list_source.setCurrentIndex(i)
			self.add_calculation_ui.other_settings.connect(self.update_after_insertion)
			# self.add_calculation_ui.update_preview()
			self.add_calculation_ui.show()
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			self.add_proof_ui = AddProof()
			self.add_proof_ui.input_question.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[0]))
			self.add_proof_ui.input_answer.setPlainText(myfun.transform_latex_to_plaintext(self.question_data_in_ModifyBox[1]))
			i = 0
			while self.question_data_in_ModifyBox[2] != self.sections[i][0]:
				i += 1
			self.add_proof_ui.list_section.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[3] != self.difficulties[i][0]:
				i += 1
			self.add_proof_ui.list_difficulty.setCurrentIndex(i)
			i = 0
			while self.question_data_in_ModifyBox[4] != self.sources[i][0]:
				i += 1
			self.add_proof_ui.list_source.setCurrentIndex(i)
			self.add_proof_ui.other_settings.connect(self.update_after_insertion)
			# self.add_proof_ui.update_preview()
			self.add_proof_ui.show()

	def tree_sections_clicked(self):
		currentItem = self.tree_sections.currentItem()
		if currentItem in self.roots_in_BrowseBox: # 如果点击的是章
			if (not currentItem.isSelected()) and (currentItem in self.chapters_selected_previously): # 如果上次选中，这次没选中，则设置所有子节点未选中
				self.chapters_selected_previously.remove(currentItem)
				for i in range(currentItem.childCount()):
					currentItem.child(i).setSelected(False)
			elif (currentItem.isSelected()) and (currentItem not in self.chapters_selected_previously): # 如果上次未选中，这次选中，则设置所有子节点选中
				self.chapters_selected_previously.append(currentItem)
				for i in range(currentItem.childCount()):
					currentItem.child(i).setSelected(True)
		else: # 如果点击的是节
			if (not currentItem.isSelected()) and currentItem.parent().isSelected(): # 如果点击的节取消选中，且其父节点章被选中，则设置父节点为未选中
				currentItem.parent().setSelected(False)
				self.chapters_selected_previously.remove(currentItem.parent())
		items = self.tree_sections.selectedItems()
		self.selected_sectionsid_in_BrowseBox = []
		for item in items:
			if item not in self.roots_in_BrowseBox: # 不是父节点的话
				i = 0
				while item.text(0) != self.sections[i][1]:
					i = i + 1
				self.selected_sectionsid_in_BrowseBox.append(self.sections[i][0])
			else:
				pass
		self.update_preview_in_BrowseBox()

	def tree_sections_in_ModifyBox_clicked(self):
		currentItem = self.tree_sections_in_ModifyBox.currentItem()
		if currentItem.isSelected():
			if currentItem not in self.roots_in_ModifyBox:
				i = 0
				while currentItem.text(0) != self.sections[i][1]:
					i += 1
				self.sectionid_selected_in_ModifyBox = self.sections[i][0]
			else:
				self.sectionid_selected_in_ModifyBox = 0
		else:
			self.sectionid_selected_in_ModifyBox = 0
		self.retrieve_questionids_in_ModifyBox()

	def update_total_questions_sum(self): # 更新当前各类问题总数
		searchstring = ('select count(*) from schoice')
		num_schoice = mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_schoice))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 0, newItem)
		searchstring = ('select count(*) from mchoice')
		num_mchoice = mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_mchoice))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 1, newItem)
		searchstring = ('select count(*) from tof')
		num_tof = mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_tof))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 2, newItem)
		searchstring = ('select count(*) from blank')
		num_blank = mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_blank))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 3, newItem)
		searchstring = ('select count(*) from calculation')
		num_calculation = mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_calculation))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 4, newItem)
		searchstring = ('select count(*) from proof')
		num_proof = mydb.search(searchstring)[0][0]
		newItem = QTableWidgetItem(str(num_proof))
		newItem.setTextAlignment(Qt.AlignHCenter)
		self.tbl_total_questions_num.setItem(0, 5, newItem)

	def update_after_insertion(self, other_settings): # 添加题目后主界面更新
		self.last_added_section_id = other_settings[0]
		self.last_added_difficulty_id = other_settings[1]
		self.last_added_source_id = other_settings[2]
		self.update_total_questions_sum()
		self.update_preview_in_BrowseBox()
		self.retrieve_questionids_in_ModifyBox()
		self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)

	def update_after_modification(self, other_settings): # 修改题目后主界面更新
		if self.sectionid_selected_in_ModifyBox != other_settings[0]:
			index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
			self.questionids_in_ModifyBox.remove(self.questionid_in_ModifyBox)
			if len(self.questionids_in_ModifyBox) == 0:
				self.questionid_in_ModifyBox = 0
			elif index == len(self.questionids_in_ModifyBox):
				self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index - 1]
			else:
				self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[index]
		self.update_preview_in_BrowseBox()
		self.update_preview_in_ModifyBox()
		self.update_sections_in_ExportBox(self.selected_sectionids_in_ExportBox)

	def update_sections_in_ExportBox(self, sectionids):
		self.selected_sectionids_in_ExportBox = sectionids
		self.tbl_selectedsections.setRowCount(len(sectionids))
		total_num_schoice = 0
		total_num_mchoice = 0
		total_num_tof = 0
		total_num_blank = 0
		total_num_calculation = 0
		total_num_proof = 0
		for i in range(len(sectionids)):
			j = 0
			while self.sections[j][0] != sectionids[i]:
				j = j + 1
			newItem = QTableWidgetItem(self.sections[j][1])
			self.tbl_selectedsections.setItem(i, 0, newItem)
			searchstring = ('select count(*) from schoice where section=%d' % (sectionids[i]))
			num_schoice = mydb.search(searchstring)[0][0]
			total_num_schoice = total_num_schoice + num_schoice
			newItem = QTableWidgetItem(str(num_schoice))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 1, newItem)
			searchstring = ('select count(*) from mchoice where section=%d' % (sectionids[i]))
			num_mchoice = mydb.search(searchstring)[0][0]
			total_num_mchoice = total_num_mchoice + num_mchoice
			newItem = QTableWidgetItem(str(num_mchoice))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 2, newItem)
			searchstring = ('select count(*) from tof where section=%d' % (sectionids[i]))
			num_tof = mydb.search(searchstring)[0][0]
			total_num_tof = total_num_tof + num_tof
			newItem = QTableWidgetItem(str(num_tof))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 3, newItem)
			searchstring = ('select count(*) from blank where section=%d' % (sectionids[i]))
			num_blank = mydb.search(searchstring)[0][0]
			total_num_blank = total_num_blank + num_blank
			newItem = QTableWidgetItem(str(num_blank))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 4, newItem)
			searchstring = ('select count(*) from calculation where section=%d' % (sectionids[i]))
			num_calculation = mydb.search(searchstring)[0][0]
			total_num_calculation = total_num_calculation + num_calculation
			newItem = QTableWidgetItem(str(num_calculation))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 5, newItem)
			searchstring = ('select count(*) from proof where section=%d' % (sectionids[i]))
			num_proof = mydb.search(searchstring)[0][0]
			total_num_proof = total_num_proof + num_proof
			newItem = QTableWidgetItem(str(num_proof))
			newItem.setTextAlignment(Qt.AlignHCenter)
			self.tbl_selectedsections.setItem(i, 6, newItem)
		self.ed_schoice.setText(str(total_num_schoice))
		self.ed_mchoice.setText(str(total_num_mchoice))
		self.ed_tof.setText(str(total_num_tof))
		self.ed_blank.setText(str(total_num_blank))
		self.ed_calculate.setText(str(total_num_calculation))
		self.ed_prove.setText(str(total_num_proof))

	def update_preview_in_ModifyBox(self):
		# print('sectionid:%d,questionid:%d' % (self.sectionid_selected_in_ModifyBox,self.questionid_in_ModifyBox))
		if self.sectionid_selected_in_ModifyBox == 0 or self.questionid_in_ModifyBox == 0:
			self.btn_next.setEnabled(False)
			self.btn_previous.setEnabled(False)
			self.btn_modify.setEnabled(False)
			self.btn_delete.setEnabled(False)
			self.btn_copy.setEnabled(False)
			self.lbl_sequence_in_ModifyBox.setText('题目序列：0/0')
			self.webView_in_ModifyBox.setHtml(myfun.gethtml(self.webView_in_ModifyBox.width()))
			return
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation where id=%d' % (self.questionid_in_ModifyBox))
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof where id=%d' % (self.questionid_in_ModifyBox))
		thisquestion = mydb.search(searchstring)
		self.question_data_in_ModifyBox = [i for i in thisquestion[0]]
		questionstring = myfun.format_questiondata_to_html(self.question_data_in_ModifyBox, self.list_type_of_question_in_ModifyBox.currentText(), fromdatabase=1)
		pageSourceContent = questionstring
		self.webView_in_ModifyBox.setHtml(myfun.gethtml(self.webView_in_ModifyBox.width(), pageSourceContent))
		index = self.questionids_in_ModifyBox.index(self.questionid_in_ModifyBox)
		self.btn_previous.setEnabled(index != 0)
		self.btn_modify.setEnabled(True)
		self.btn_delete.setEnabled(True)
		self.btn_copy.setEnabled(True)
		self.btn_next.setEnabled(index != len(self.questionids_in_ModifyBox)-1)
		self.lbl_sequence_in_ModifyBox.setText('题目序列：%d/%d' % (index+1, len(self.questionids_in_ModifyBox)))

	# 更新预览
	def update_preview_in_BrowseBox(self):
		if not self.selected_sectionsid_in_BrowseBox:
			self.webView_in_BrowseBox.setHtml(myfun.gethtml(self.webView_in_BrowseBox.width()))
			return
		sectionstring = (' where section=' + str(self.selected_sectionsid_in_BrowseBox[0]))
		for i in self.selected_sectionsid_in_BrowseBox:
			sectionstring = sectionstring + ' or section=' + str(i)
		# 读单选题表
		searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice' + sectionstring)
		schoice = mydb.search(searchstring)
		num_schoice = len(schoice)
		# 读多选题表
		searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice' + sectionstring)
		mchoice = mydb.search(searchstring)
		num_mchoice = len(mchoice)
		# 读判断题表
		searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof' + sectionstring)
		tof = mydb.search(searchstring)
		num_tof = len(tof)
		# 读填空题表
		searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank' + sectionstring)
		blank = mydb.search(searchstring)
		num_blank = len(blank)
		# 读计算题表
		searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation' + sectionstring)
		calculation = mydb.search(searchstring)
		num_calculation = len(calculation)
		# 读证明题表
		searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof' + sectionstring)
		proof = mydb.search(searchstring)
		num_proof = len(proof)

		if not (num_schoice or num_mchoice or num_tof or num_blank or num_calculation or num_proof):
			self.webView_in_BrowseBox.setHtml(myfun.gethtml(self.webView_in_BrowseBox.width()))
			return
		
		pageSourceContent = ''
		# 写入单选题
		if self.chk_schoice_in_BrowseBox.isChecked():
			if num_schoice>0:
				pageSourceContent += ('</p><h2>单选题</h2>')
				for i in range(num_schoice):
					thisquestion = [j for j in schoice[i]]
					questionstring = myfun.format_questiondata_to_html(thisquestion, '单选题', str(i+1), fromdatabase=1)
					pageSourceContent += questionstring

		# 写入多选题
		if self.chk_mchoice_in_BrowseBox.isChecked():
			if num_mchoice>0:
				pageSourceContent += ('</p><h2>多选题</h2>')
				for i in range(num_mchoice):
					thisquestion = [j for j in mchoice[i]]
					questionstring = myfun.format_questiondata_to_html(thisquestion, '多选题', str(i+1), fromdatabase=1)
					pageSourceContent += questionstring

		# 写入判断题
		if self.chk_tof_in_BrowseBox.isChecked():
			if num_tof>0:
				pageSourceContent += ('</p><h2>判断题</h2>')
				answertext = ['错误', '正确']
				for i in range(num_tof):
					thisquestion = [j for j in tof[i]]
					questionstring = myfun.format_questiondata_to_html(thisquestion, '判断题', str(i+1), fromdatabase=1)
					pageSourceContent += questionstring

		# 写入填空题
		if self.chk_blank_in_BrowseBox.isChecked():
			if num_blank>0:
				pageSourceContent += ('</p><h2>填空题</h2>')
				for i in range(num_blank):
					thisquestion = [j for j in blank[i]]
					questionstring = myfun.format_questiondata_to_html(thisquestion, '填空题', str(i+1), fromdatabase=1)
					pageSourceContent += questionstring

		# 写入计算题
		if self.chk_calculation_in_BrowseBox.isChecked():
			if num_calculation>0:
				pageSourceContent += ('</p><h2>计算题</h2>')
				for i in range(num_calculation):
					thisquestion = [j for j in calculation[i]]
					questionstring = myfun.format_questiondata_to_html(thisquestion, '计算题', str(i+1), fromdatabase=1)
					pageSourceContent += questionstring

		# 写入证明题
		if self.chk_proof_in_BrowseBox.isChecked():
			if num_proof>0:
				pageSourceContent += ('</p><h2>证明题</h2>')
				for i in range(num_proof):
					thisquestion = [j for j in proof[i]]
					questionstring = myfun.format_questiondata_to_html(thisquestion, '证明题', str(i+1), fromdatabase=1)
					pageSourceContent += questionstring

		self.webView_in_BrowseBox.setHtml(myfun.gethtml(self.webView_in_BrowseBox.width(), pageSourceContent))

	def retrieve_data(self):
		searchstring = 'select * from chapters'
		self.chapters = mydb.search(searchstring)
		searchstring = 'select * from sections'
		self.sections = mydb.search(searchstring)
		searchstring = 'select * from difficulties'
		self.difficulties = mydb.search(searchstring)
		searchstring = 'select * from sources'
		self.sources = mydb.search(searchstring)

	def retrieve_questionids_in_ModifyBox(self):
		if self.sectionid_selected_in_ModifyBox == 0:
			self.update_preview_in_ModifyBox()
			return
		if self.list_type_of_question_in_ModifyBox.currentText() == '单选题':
			searchstring = ('select "id" from schoice where section = %d' % (self.sectionid_selected_in_ModifyBox))
			schoice = mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in schoice] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '多选题':
			searchstring = ('select "id" from mchoice where section = %d' % (self.sectionid_selected_in_ModifyBox))
			mchoice = mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in mchoice] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '判断题':
			searchstring = ('select "id" from tof where section = %d' % (self.sectionid_selected_in_ModifyBox))
			tof = mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in tof] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '填空题':
			searchstring = ('select "id" from blank where section = %d' % (self.sectionid_selected_in_ModifyBox))
			blank = mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in blank] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '计算题':
			searchstring = ('select "id" from calculation where section = %d' % (self.sectionid_selected_in_ModifyBox))
			calculation = mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in calculation] # 指定章节指定题型的所有id列表
		if self.list_type_of_question_in_ModifyBox.currentText() == '证明题':
			searchstring = ('select "id" from proof where section = %d' % (self.sectionid_selected_in_ModifyBox))
			proof = mydb.search(searchstring)
			self.questionids_in_ModifyBox = [i[0] for i in proof] # 指定章节指定题型的所有id列表
		if self.questionids_in_ModifyBox:
			self.questionid_in_ModifyBox = self.questionids_in_ModifyBox[0]
		else:
			self.questionid_in_ModifyBox = 0
		self.update_preview_in_ModifyBox()

	def transmit_settings(self, ui): # 将设置传递给打开的子窗口
		ui.other_settings.connect(self.update_after_insertion)
		i = 0
		while self.last_added_section_id != self.sections[i][0]:
			i += 1
		ui.list_section.setCurrentIndex(i)
		i = 0
		while self.last_added_difficulty_id != self.difficulties[i][0]:
			i += 1
		ui.list_difficulty.setCurrentIndex(i)
		i = 0
		while self.last_added_source_id != self.sources[i][0]:
			i += 1
		ui.list_source.setCurrentIndex(i)
	
	def export_questions(self):
		if not self.selected_sectionids_in_ExportBox:
			QMessageBox.about(self, u'通知', u'请先选择章节！')
			return
		sectionstring = (' where section=' + str(self.selected_sectionids_in_ExportBox[0]))
		for i in range(1, len(self.selected_sectionids_in_ExportBox)):
			sectionstring = sectionstring + ' or section=' + str(self.selected_sectionids_in_ExportBox[i])
		# 读单选题表
		searchstring = ('select "question", "A", "B", "C", "D", "answer", "explain", "section", "difficulty", "source" from schoice' + sectionstring)
		schoice = mydb.search(searchstring)
		num_schoice = len(schoice)
		# 读多选题表
		searchstring = ('select "question", "A", "B", "C", "D", "pos_A", "pos_B", "pos_C", "pos_D", "explain", "section", "difficulty", "source" from mchoice' + sectionstring)
		mchoice = mydb.search(searchstring)
		num_mchoice = len(mchoice)
		# 读判断题表
		searchstring = ('select "question", "correct", "explain", "section", "difficulty", "source" from tof' + sectionstring)
		tof = mydb.search(searchstring)
		num_tof = len(tof)
		# 读填空题表
		searchstring = ('select "question", "answer1", "answer2", "answer3", "answer4", "explain", "section", "difficulty", "source" from blank' + sectionstring)
		blank = mydb.search(searchstring)
		num_blank = len(blank)
		# 读计算题表
		searchstring = ('select "question", "answer", "section", "difficulty", "source" from calculation' + sectionstring)
		calculation = mydb.search(searchstring)
		num_calculation = len(calculation)
		# 读证明题表
		searchstring = ('select "question", "answer", "section", "difficulty", "source" from proof' + sectionstring)
		proof = mydb.search(searchstring)
		num_proof = len(proof)

		if not (num_schoice or num_mchoice or num_tof or num_blank or num_calculation or num_proof):
			QMessageBox.about(self, u'通知', u'当前章节中没有题目！')
			return
		
		try:
			f = open('myquestions.tex', 'w', encoding='utf-8')
			# 写入单选题
			if num_schoice>0:
				f.writelines('\\section{单项选择题}\n')
				f.writelines('\\begin{enumerate}\n')
				for i in range(num_schoice):
					f.writelines('\t\\item %s\n' % (schoice[i][0]))
					maxlen = max(myfun.mathlength(schoice[i][1]), myfun.mathlength(schoice[i][2]), myfun.mathlength(schoice[i][3]), myfun.mathlength(schoice[i][4]))
					para = 4
					if maxlen > 32:
						para = 1
					elif maxlen > 14:
						para = 2
					f.writelines('\t\t\\begin{choice}(%d)\n' % (para))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][1]))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][2]))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][3]))
					f.writelines('\t\t\t\\choice %s\n' % (schoice[i][4]))
					f.writelines('\t\t\\end{choice}\n')
				f.writelines('\\end{enumerate}\n')
			# 写入多选题
			if num_mchoice>0:
				f.writelines('\\section{多项选择题}\n')
				f.writelines('\\begin{enumerate}\n')
				for i in range(num_mchoice):
					f.writelines('\t\\item %s\n' % (mchoice[i][0]))
					maxlen = max(myfun.mathlength(mchoice[i][1]), myfun.mathlength(mchoice[i][2]), myfun.mathlength(mchoice[i][3]), myfun.mathlength(mchoice[i][4]))
					para = 4
					if maxlen > 32:
						para = 1
					elif maxlen > 14:
						para = 2
					f.writelines('\t\t\\begin{choice}(4)\n')
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][1]))
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][2]))
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][3]))
					f.writelines('\t\t\t\\choice %s\n' % (mchoice[i][4]))
					f.writelines('\t\t\\end{choice}\n')
				f.writelines('\\end{enumerate}\n')
			# 写入判断题
			if num_tof>0:
				f.writelines('\\section{判断题}\n')
				f.writelines('\\begin{enumerate}\n')
				for i in range(num_tof):
					f.writelines('\t\\item %s \\hfill\\emptychoice \n' % (tof[i][0]))
				f.writelines('\\end{enumerate}\n')
			# 写入填空题
			if num_blank>0:
				f.writelines('\\section{填空题}\n')
				f.writelines('\\begin{enumerate}\n')
				for i in range(num_blank):
					f.writelines('\t\\item %s\n' % (blank[i][0]))
				f.writelines('\\end{enumerate}\n')
			# 写入计算题
			if num_calculation>0:
				f.writelines('\\section{计算题}\n')
				f.writelines('\\begin{enumerate}\n')
				for i in range(num_calculation):
					f.writelines('\t\\item %s\n' % (calculation[i][0]))
				f.writelines('\\end{enumerate}\n')
			# 写入证明题
			if num_proof>0:
				f.writelines('\\section{证明题}\n')
				f.writelines('\\begin{enumerate}\n')
				for i in range(num_proof):
					f.writelines('\t\\item %s\n' % (proof[i][0]))
				f.writelines('\\end{enumerate}\n')

			# 写入解答
			if self.chk_solution.isChecked():
				# 单选题解答
				if num_schoice>0:
					f.writelines('\\section{单项选择题解答}\n')
					f.writelines('\\begin{enumerate}\n')
					for i in range(num_schoice):
						if schoice[i][6] != '':
							f.writelines('\t\\item %s\\\\\n' % (schoice[i][5]))
							f.writelines('\t\t解析：%s\n' % (schoice[i][6]))
						else:
							f.writelines('\t\\item %s\n' % (schoice[i][5]))
					f.writelines('\\end{enumerate}\n')
				# 多选题解答
				if num_mchoice>0:
					f.writelines('\\section{多项选择题解答}\n')
					f.writelines('\\begin{enumerate}\n')
					for i in range(num_mchoice):
						answer = ''
						answer_raw = mchoice[i][5:9]
						for j in range(1, max(answer_raw)+1):
							thisanswer = ''
							for k in range(4):
								if answer_raw[k] == j:
									thisanswer = thisanswer + chr(k+65)
							answer = answer + '第'+str(j)+'空：' + thisanswer + '；' 
						if mchoice[i][9] != '':
							f.writelines('\t\\item %s\\\\\n' % (answer))
							f.writelines('\t\t解析：%s\n' % (mchoice[i][9]))
						else:
							f.writelines('\t\\item %s\n' % (answer))
					f.writelines('\\end{enumerate}\n')
				# 判断题解答
				if num_tof>0:
					f.writelines('\\section{判断题解答}\n')
					f.writelines('\\begin{enumerate}\n')
					for i in range(num_tof):
						answer = ['错误', '正确']
						if tof[i][2] != '':
							f.writelines('\t\\item %s\\\\\n' % (answer(tof[i][1])))
							f.writelines('\t\t解析：%s\n' % (tof[i][2]))
						else:
							f.writelines('\t\\item %s\n' % (answer(tof[i][1])))
					f.writelines('\\end{enumerate}\n')
				# 填空题解答
				if num_blank>0:
					f.writelines('\\section{填空题解答}\n')
					f.writelines('\\begin{enumerate}\n')
					for i in range(num_blank):
						if blank[i][5] != '':
							if blank[i][4] != '':
								f.writelines('\t\\item %s；%s；%s；%s\\\\\n' % (blank[i][1],blank[i][2],blank[i][3],blank[i][4]))
							elif blank[i][3] != '':
								f.writelines('\t\\item %s；%s；%s\\\\\n' % (blank[i][1],blank[i][2],blank[i][3]))
							elif blank[i][2] != '':
								f.writelines('\t\\item %s；%s\\\\\n' % (blank[i][1],blank[i][2]))
							else:
								f.writelines('\t\\item %s\\\\\n' % (blank[i][1]))
							f.writelines('\t\t解析：%s\n' % (blank[i][5]))
						else:
							if blank[i][4] != '':
								f.writelines('\t\\item %s；%s；%s；%s\n' % (blank[i][1],blank[i][2],blank[i][3],blank[i][4]))
							elif blank[i][3] != '':
								f.writelines('\t\\item %s；%s；%s\n' % (blank[i][1],blank[i][2],blank[i][3]))
							elif blank[i][2] != '':
								f.writelines('\t\\item %s；%s\n' % (blank[i][1],blank[i][2]))
							else:
								f.writelines('\t\\item %s\n' % (blank[i][1]))
					f.writelines('\\end{enumerate}\n')
				# 计算题解答
				if num_calculation>0:
					f.writelines('\\section{计算题解答}\n')
					f.writelines('\\begin{enumerate}\n')
					for i in range(num_calculation):
						if calculation[i][1] == '':
							f.writelines('\t\\item 解：略\n')
						else:
							f.writelines('\t\\item 解：%s\n' % (calculation[i][1]))
					f.writelines('\\end{enumerate}\n')
				# 证明题解答
				if num_proof>0:
					f.writelines('\\section{计算题解答}\n')
					f.writelines('\\begin{enumerate}\n')
					for i in range(num_proof):
						if proof[i][1] != '':
							f.writelines('\t\\item 证明：%s\n' % (proof[i][1]))
						else:
							f.writelines('\t\\item 证明：略\n')
					f.writelines('\\end{enumerate}\n')
			f.close()
			QMessageBox.about(self, u'通知', u'导出成功！')
		except Exception as e:
			print(e)
			QMessageBox.about(self, u'错误', u'导出失败！')
			return

	# 调整窗口大小事件
	def resizeEvent(self, event):#调整窗口尺寸时，该方法被持续调用。event参数包含QResizeEvent类的实例，通过该类的下列方法获得窗口信息：
		self.update_preview_in_BrowseBox()
		self.update_preview_in_ModifyBox()