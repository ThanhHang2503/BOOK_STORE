n= int(input("nhap so phan tu"))
list=[]

for i in range (n): 
    value= int(input("nhap ptu thu {i}"))
    list.append(value)
    
tong = 0  
for i in range (n):
    tong+= list[i]
print(tong)
dem=0   
for i in range (n):
    if(list[i]<5):
        dem+=1
print(dem)

list.pop()
list.remove()