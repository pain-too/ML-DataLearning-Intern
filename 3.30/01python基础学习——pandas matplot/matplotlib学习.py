import matplotlib.pyplot as plt
from matplotlib import rcParams


#更改字体
rcParams['font.family']='Songti SC'

#添加数据
plt.figure(figsize=(10,5))
month = ['一月','二月','三月','四月']
sales = [20,30,18,27]


#绘图             #添加图例，说明图线归属
plt.plot(month,sales,label='产品A')
plt.legend(loc='upper left')


#添加标题
plt.title('销售额',color='red',fontsize = 24)

#添加坐标轴说明
plt.xlabel('月份',fontsize=20,color='green')
plt.ylabel('销量/万元',fontsize=20,color='blue')

#添加网格线
#plt.grid(True)代表横纵都画
#plt.grid(axis='x')只有竖线
plt.grid(axis='y',alpha=0.5,linestyle='--')#alpha是透明度，颜色变浅

#设置刻度字体大小，设置旋转
plt.xticks(rotation=60,fontsize=18)
plt.yticks(rotation = 20,fontsize=18)

#设置y轴刻度范围
plt.ylim(0,50)

#每个点标上坐标（具体数据）
for x,y in zip(month,sales):
    print(x,y)
    plt.text(x,y,str(y),ha='center',va='bottom',fontsize=20,color='blue')
plt.show()


