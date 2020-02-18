def 完善信息（）：
    self.简历处理（）
    self.信息储存（）

def 简历处理（）：
     f = open('../简历.word',"w")
     f.write(简历内容)
     return 保存路径

def 信息储存（）：
     找到求职者，写入姓名，期望薪资，期望岗位，简历保存的路径
	