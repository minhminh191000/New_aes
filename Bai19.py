#Bài 9: Viết chương trình Python giải phương trình bậc 2: ax2 + bx + c = 0.
import math
def ptbac2(a,b,c):
    Den_ta=(b**2)-(4*a*c)
    print(Den_ta)
    if Den_ta>0 :
        x1=(b + math.sqrt(Den_ta))/(2*a)
        x2=(b - math.sqrt(Den_ta))/(2*a)
        return " pt có 2 nghiệm {0},{1}".format(x1,x2)
    elif Den_ta==0:
        x=b/(2*a)
        return " pt có 1 nghiệm {0}".format(x)
    else:
        return " vô nghiệm"
a = int(input('nhập hệ số a : '))
b = int(input('nhập hệ số b : '))
c = int(input('nhập hệ số c : '))
print(ptbac2(a,b,c))